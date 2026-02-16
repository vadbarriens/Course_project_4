from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from client.models import Client
from mailings.models import Mailing, Message
from users.models import CustomUser


class Command(BaseCommand):
    """Кастомная команда по созданию группы Менеджеры с нужными правами"""

    help = "Создаёт группу Менеджеры с нужными правами"

    def handle(self, *args, **kwargs):
        """Создание прав доступа"""
        group, created = Group.objects.get_or_create(name="Менеджеры")
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Группа "Менеджеры" создана'))
        else:
            self.stdout.write('⚠️ Группа "Менеджеры" уже существует')

        # Права только на просмотр
        models = [Mailing, Message, Client, CustomUser]
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            view_permission = Permission.objects.get(
                codename=f"view_{model.__name__.lower()}",
                content_type=content_type,
            )
            group.permissions.add(view_permission)

        # Отдельное право: блокировка пользователей
        users_content_type = ContentType.objects.get_for_model(CustomUser)
        block_perm = Permission.objects.get(
            codename="can_block_users",
            content_type=users_content_type,
        )
        group.permissions.add(block_perm)

        self.stdout.write(self.style.SUCCESS("🎉 Права добавлены"))
