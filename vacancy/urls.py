from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_edit/', views.profile_edit_view, name='profile_edit'),
    path('companies/', views.companies_list, name='companies_list'),
    path('company/<int:company_id>/', views.company_detail, name='company_detail'),
    path('vacancies/', views.create_and_list_vacancies, name='create_vacancy'),
    path('vacancies/<int:vacancy_id>/', views.vacancy_detail, name='vacancy_detail'),
    path('vacancy/edit/<int:vacancy_id>/', views.edit_vacancy, name='edit_vacancy'),
    path('vacancy/delete/<int:vacancy_id>/', views.delete_vacancy, name='delete_vacancy'),
]
