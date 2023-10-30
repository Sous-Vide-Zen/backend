from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','is_banned')  # Определите, какие поля отображать в списке
    list_filter = ('is_admin', 'is_staff', 'is_banned')  # Добавьте фильтры
    search_fields = ('username', 'email')  # Добавьте поле поиска

admin.site.register(CustomUser, CustomUserAdmin)



