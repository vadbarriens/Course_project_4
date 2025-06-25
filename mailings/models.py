from django.conf import settings
from django.db import models

from client.models import Client


class Message(models.Model):
    """Модель - Сообщения"""

    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        default=1,
    )

    def __str__(self):
        """Строковое представление сообщения"""
        return self.subject


class Mailing(models.Model):
    """Модель - Рассылки"""

    STATUS_CHOICES = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Создана")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_cancel_mailing", "Can cancel mailing"),
            ("can_see_all_mailings", "Can see all mailings"),
        ]

    def __str__(self):
        """Строковое представление рассылки"""
        return f"Рассылка {self.pk} ({self.status})"


class MailingAttempt(models.Model):
    """Модель - Попытка рассылок"""

    STATUS_CHOICES = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]

    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="attempts"
    )

    def __str__(self):
        """Строковое представление попыток рассылки"""
        return f"Попытка {self.mailing_id} - {self.status}"
