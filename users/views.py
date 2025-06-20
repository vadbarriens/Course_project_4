from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    """Класс для регистрации пользователя"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Переопределение метода валидации"""
        response = super().form_valid(form)
        print("Пробую отправить письмо на:", form.cleaned_data["email"])
        print("SMTP USER:", repr(settings.EMAIL_HOST_USER))
        print("SMTP PASS:", repr(settings.EMAIL_HOST_PASSWORD))

        send_mail(
            subject="🎉 Добро пожаловать в сервис рассылок!",
            message=(
                f"Здравствуйте, {form.cleaned_data['username']}!\n\n"
                f"Вы успешно зарегистрировались. "
                f"Теперь вы можете создавать клиентов, сообщения и управлять рассылками!\n\n"
                f"Если вы не регистрировались, просто проигнорируйте это письмо.\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[form.cleaned_data["email"]],
            fail_silently=False,
        )

        return response


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
