from django.core.exceptions import PermissionDenied


class ManagerCheckMixin:
    """Общий миксин для проверки роли менеджера (группа 'Менеджеры')."""

    manager_group_name = "Менеджеры"

    def is_manager(self) -> bool:
        user = getattr(self.request, "user", None)
        return bool(
            user
            and user.is_authenticated
            and user.groups.filter(name=self.manager_group_name).exists()
        )


class ManagerForbiddenMixin(ManagerCheckMixin):
    """Запрещает доступ менеджеру (возвращает 403)."""

    def dispatch(self, request, *args, **kwargs):
        if self.is_manager():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ManagerRequiredMixin(ManagerCheckMixin):
    """Разрешает доступ только менеджеру (возвращает 403)."""

    def dispatch(self, request, *args, **kwargs):
        if not self.is_manager():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

