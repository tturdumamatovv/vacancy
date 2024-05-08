from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import CustomUser, SocialLink, Company, Vacancy


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password1', 'password2')


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1']


class ProfileEditForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm border px-4 py-2',
    }))
    resume = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm border px-4 py-2',
    }))

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'location', 'gender', 'birth_date', 'resume']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm border px-4 py-2',
                'placeholder': 'Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm border px-4 py-2',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm border px-4 py-2',
                'placeholder': 'Phone'
            }),
            'location': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm border px-4 py-2',
                'placeholder': 'Location'
            }),
            'gender': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm border px-4 py-2'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm border px-4 py-2',
                'type': 'date'
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm border px-4 py-2'
            }),
        }


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['url', 'name']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'logo']


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'salary', 'employment_type', 'location']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Название вакансии',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Описание',
                'required': True,
                'rows': 2,
                'cols': 50
            }),
            'salary': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Зарплата',
            }),
            'employment_type': forms.Select(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Тип занятости',
                'required': True
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Местоположение',
            }),
        }


