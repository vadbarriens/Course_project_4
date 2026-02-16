def roles(request):
    user = getattr(request, "user", None)
    is_manager = bool(user and user.is_authenticated and user.groups.filter(name="Менеджеры").exists())
    return {"is_manager": is_manager}

