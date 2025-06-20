from django.contrib import admin
from .models import Message, Mailing, MailingAttempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Создание класса для отображения сообщения в админке"""
    list_display = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Создание класса для отображения рассылок в админке"""
    list_display = ("id", "start_time", "end_time", "status")
    list_filter = ("status",)
    filter_horizontal = ("clients",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    """Создание класса для отображения попыток рассылки в админке"""
    list_display = ("mailing", "time", "status", "server_response")
    list_filter = ("status", "mailing")
