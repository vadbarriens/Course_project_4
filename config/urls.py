from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from mailings.views import home_view

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("client/", include("client.urls", namespace="clients")),
                  path("mailings/", include("mailings.urls", namespace="mailings")),
                  path("", include("mailings.urls", namespace="mailings")),
                  path("users/", include("users.urls", namespace="users")),
                  path("", home_view, name="home"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
