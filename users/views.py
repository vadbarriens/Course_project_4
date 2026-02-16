from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CustomUserCreationForm
from .models import CustomUser


def _is_manager(user: CustomUser) -> bool:
    return user.is_authenticated and user.groups.filter(name="Менеджеры").exists()


class RegisterView(CreateView):
    """Класс для регистрации пользователя"""

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Переопределение метода валидации"""
        response = super().form_valid(form)
        send_mail(
            subject="🎉 Добро пожаловать в сервис рассылок!",
            message=(
                f"Здравствуйте!\n\n"
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
    fields = ["email"]
    template_name = "users/profile_form.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        """Переопределение метода получения объекта"""
        return self.request.user


class UsersListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = "users/users_list.html"
    context_object_name = "users"
    permission_required = "users.view_customuser"

    def has_permission(self):
        # список пользователей видит только менеджер (и только при наличии permission)
        user = self.request.user
        return _is_manager(user) and user.has_perm("users.view_customuser")


class UserBlockView(PermissionRequiredMixin, UserPassesTestMixin, View):
    permission_required = "users.can_block_users"

    def test_func(self):
        return _is_manager(self.request.user)

    def post(self, request: HttpRequest, *args: str, **kwargs):
        user = get_object_or_404(CustomUser, email=self.kwargs.get("email"))
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
            messages.success(self.request, "Пользователь успешно разблокирован!")
        else:
            user.is_active = False
            user.save(update_fields=["is_active"])
            messages.success(self.request, "Пользователь успешно заблокирован!")
        return redirect("users:users_list")
