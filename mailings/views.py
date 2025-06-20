from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.cache import cache_page

from client.models import Client
from mailings.models import Mailing, MailingAttempt, Message


@cache_page(60 * 2)  # кеш на 2 минуты
def home_view(request):
    """ Главная страница сайта """
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="Запущена").count()
    unique_clients = Client.objects.values("email").distinct().count()

    return render(
        request,
        "mailings/home.html",
        {
            "total_mailings": total_mailings,
            "active_mailings": active_mailings,
            "unique_clients": unique_clients,
        },
    )


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения списка рассылок"""
    model = Mailing
    template_name = "mailings/mailing_list.html"

    def get_queryset(self):
        """Переопределение метода получения ответа """
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения детальной информации рассылки"""
    model = Mailing
    template_name = "mailings/mailing_detail.html"

    def get_queryset(self):
        """Переопределение метода получения ответа """
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания рассылки"""
    model = Mailing
    fields = ["start_time", "end_time", "status", "message", "clients"]
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        """Переопределение метода валидации """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для обновления рассылки"""
    model = Mailing
    fields = ["start_time", "end_time", "status", "message", "clients"]
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        """Переопределение метода получения ответа """
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления рассылки"""
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        """Переопределение метода получения ответа """
        return Mailing.objects.filter(owner=self.request.user)


class MailingSendView(LoginRequiredMixin, View):
    """Контроллер для отображения попытки отправки рассылки"""

    def get(self, request, pk):
        """Переопределение метода отправки запроса """
        mailing = get_object_or_404(Mailing, pk=pk)

        if mailing.owner != request.user:
            messages.error(request, "У вас нет прав на отправку этой рассылки.")
            return redirect("mailings:mailing_detail", pk=pk)

        clients = mailing.clients.all()
        success_count = 0

        for client in clients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=None,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                status = "Успешно"
                response = "OK"
                success_count += 1
            except Exception as e:
                status = "Не успешно"
                response = str(e)

            MailingAttempt.objects.create(
                mailing=mailing,
                status=status,
                server_response=response,
            )

        mailing.status = "Запущена"
        mailing.save()

        messages.success(
            request,
            f"Рассылка отправлена. Успешно: {success_count}/{clients.count()}",
        )
        return redirect("mailings:mailing_detail", pk=pk)


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения списка сообщений"""
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        """Переопределение метода получения ответа """
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания сообщения"""
    model = Message
    fields = ["subject", "body"]
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        """Переопределение метода валидации """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения детальной информации сообщения"""
    model = Message
    template_name = "mailings/message_detail.html"
    context_object_name = "object"

    def get_queryset(self):
        """Переопределение метода получения ответа """
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для обновления сообщения"""
    model = Message
    fields = ["subject", "body"]
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        """Переопределение метода получения ответа """
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления сообщения"""
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        """Переопределение метода получения ответа """
        return Message.objects.filter(owner=self.request.user)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения списка попыток рассылки"""
    model = MailingAttempt
    template_name = "mailings/mailing_attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        """Переопределение метода получения ответа """
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return MailingAttempt.objects.all()
        return MailingAttempt.objects.filter(mailing__owner=user)
