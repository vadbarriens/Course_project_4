from django.urls import path

from client.apps import ClientConfig
from client.views import (ClientCreateView, ClientDeleteView, ClientDetailView,
                          ClientListView, ClientUpdateView)

app_name = ClientConfig.name

urlpatterns = [
    path("client/", ClientListView.as_view(), name="client_list"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client/create/", ClientCreateView.as_view(), name="client_create"),
    path("client/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("client/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
]
