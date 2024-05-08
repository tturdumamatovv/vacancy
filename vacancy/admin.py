from django.contrib import admin

from .models import CustomUser, SocialLink, Company, Vacancy

admin.site.register(CustomUser)
admin.site.register(SocialLink)
admin.site.register(Company)
admin.site.register(Vacancy)
