from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, name='', **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, name='', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, name, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    company = models.OneToOneField(
        "Company",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='custom_user_company'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class SocialLink(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='social_links')
    url = models.URLField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}: {self.url}"


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    owner = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='company_owner'
    )
    industry = models.CharField(max_length=50, choices=[
        ('it', 'IT'),
        ('marketing', 'Маркетинг'),
        ('construction', 'Строительство'),
        # Добавьте другие отрасли при необходимости
    ], default='', blank=True)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employment_type = models.CharField(max_length=20, choices=[
        ('full-time', 'Полная занятость'),
        ('part-time', 'Частичная занятость'),
        ('project', 'Проектная работа'),
        ('internship', 'Стажировка')
    ], default='', blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
