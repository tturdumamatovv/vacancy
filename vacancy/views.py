from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import CustomUserCreationForm, CustomLoginForm, ProfileEditForm, SocialLinkForm, VacancyForm
from .models import Company, Vacancy

from django.shortcuts import render
from .models import Vacancy, Company


def home(request):
    # Получаем значения фильтров из GET-запроса
    keyword = request.GET.get('keyword', '')
    location = request.GET.get('location', '')
    industry = request.GET.get('industry', '')
    employment_type = request.GET.get('employmentType', '')
    salary = request.GET.get('salary', '')

    # Начинаем с базового запроса на получение вакансий
    vacancies = Vacancy.objects.all()

    # Фильтрация по ключевому слову в заголовке вакансии
    if keyword:
        vacancies = vacancies.filter(title__icontains=keyword)

    # Фильтрация по местоположению
    if location:
        vacancies = vacancies.filter(location__icontains=location)

    # Фильтрация по отрасли
    if industry:
        vacancies = vacancies.filter(company__industry=industry)

    # Фильтрация по типу занятости
    if employment_type:
        vacancies = vacancies.filter(employment_type=employment_type)

    # Фильтрация по зарплате (от)
    if salary:
        vacancies = vacancies.filter(salary__gte=salary)

    # Передаем данные в шаблон
    context = {
        'keyword': keyword,
        'location': location,
        'industry': industry,
        'employment_type': employment_type,
        'salary': salary,
        'vacancies': vacancies
    }

    return render(request, 'index.html', context)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def profile_edit_view(request):
    user = request.user
    profile_form = ProfileEditForm(request.POST or None, request.FILES or None, instance=user)
    social_link_forms = [SocialLinkForm(request.POST or None, instance=social_link) for social_link in user.social_links.all()]

    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()
        else:
            print("Profile form is not valid:", profile_form.errors)

        for form in social_link_forms:
            if form.is_valid():
                form.save()
            else:
                print("Social link form is not valid:", form.errors)

        return redirect('profile')

    context = {
        'profile_form': profile_form,
        'social_link_forms': social_link_forms,
    }

    return render(request, 'edit_profile.html', context)


# Представление списка компаний
def companies_list(request):
    companies = Company.objects.all()
    return render(request, 'company.html', {'companies': companies})


# Представление деталей компании
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    vacancies = company.vacancies.all()
    return render(request, 'company_detail.html', {'company': company, 'vacancies': vacancies})


@login_required
def create_and_list_vacancies(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            if hasattr(request.user, 'company') and request.user.company is not None:
                form.instance.company = request.user.company
                form.save()
                return redirect('create_vacancy')
            else:
                form.add_error(None, "У вас нет связанной компании для создания вакансии.")
    else:
        form = VacancyForm()

    vacancies = Vacancy.objects.all()

    context = {
        'form': form,
        'vacancies': vacancies,
    }

    return render(request, 'vacancy.html', context)


@login_required
def edit_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    # Проверка, является ли текущий пользователь владельцем компании, к которой относится вакансия
    if request.user.company != vacancy.company:
        # Если пользователь не владеет вакансией, перенаправляем его или выдаем ошибку
        return redirect('home')  # Здесь можно выбрать другой маршрут или страницу для перенаправления

    if request.method == 'POST':
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect('create_vacancy')
    else:
        form = VacancyForm(instance=vacancy)

    return render(request, 'edit_vacancy.html', {'form': form, 'vacancy': vacancy})


@login_required
def delete_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    # Проверка, является ли текущий пользователь владельцем компании, к которой относится вакансия
    if request.user.company != vacancy.company:
        # Если пользователь не владеет вакансией, перенаправляем его или выдаем ошибку
        return redirect('home')  # Здесь можно выбрать другой маршрут или страницу для перенаправления

    # Удаление вакансии
    vacancy.delete()
    return redirect('create_vacancy')


def vacancy_detail(request, vacancy_id):
    # Получение вакансии по переданному идентификатору
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    # Передача данных вакансии в контексте шаблона
    context = {
        'vacancy': vacancy,
    }
    return render(request, 'vacancy_detail.html', context)