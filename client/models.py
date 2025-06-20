from django.db import models
from django.conf import settings


class Client(models.Model):
    """Модель - клиент"""
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200, verbose_name='Ф.И.О.', help_text='Введите свое Ф.И.О.')
    comment = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients",
    )

    class Meta:
        """Метаданные"""
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        """Строковое представление клиента"""
        return f'{self.full_name} - {self.email}'
