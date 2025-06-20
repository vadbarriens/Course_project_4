from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Класс для формы пользователя"""

    class Meta:
        """Метаданные"""
        model = CustomUser
        fields = ("email", "username")
