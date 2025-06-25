from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Создание класса для отображения пользователя в админке"""

    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_superuser")
    search_fields = ("email", "username")
    ordering = ("email",)
