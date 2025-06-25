import secrets

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy

from config.settings import EMAIL_HOST_USER
from .models import CustomUser
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    """Класс для регистрации пользователя"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(15)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение электронного адреса',
            message=f'Спасибо за регистрацию на нашем сайте. Подтвердите адрес электронной почты, перейдя по следующей ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class CustomLoginView(LoginView):
    """Класс для входа пользователя в систему"""
    template_name = "users/login.html"


class CustomLogoutView(LogoutView):
    """Класс для выхода пользователя в систему"""
    next_page = reverse_lazy("mailings:home")


class ProfileView(LoginRequiredMixin, DetailView):
    """Класс для отображения профиля пользователя в системе"""
    model = CustomUser
    template_name = "users/profile.html"

    def get_object(self):
        """Переопределение метода получения объекта"""
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для изменения профиля пользователя в системе"""

    model = CustomUser
    fields = ["username", "email"]
    template_name = "users/profile_form.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        """Переопределение метода получения объекта"""
        return self.request.user
