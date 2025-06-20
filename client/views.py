from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Client


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения списка клиентов"""
    model = Client
    template_name = "clients/client_list.html"

    def get_queryset(self):
        """Переопределение метода получения ответа """
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения детальной информации клиента"""
    model = Client
    template_name = "clients/client_detail.html"
    success_url = reverse_lazy("client:client_list")

    def get_queryset(self):
        """Переопределение метода получения ответа """
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для добавления клиента"""
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("client:client_list")

    def form_valid(self, form):
        """Переопределение метода валидации"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для обновления клиента"""
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("client:client_list")

    def get_queryset(self):
        """Переопределение метода получения ответа """
        return Client.objects.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления клиента"""
    model = Client
    template_name = "clients/client_delete.html"
    success_url = reverse_lazy("client:client_list")

    def get_queryset(self):
        """Переопределение метода получения ответа """
        return Client.objects.filter(owner=self.request.user)
