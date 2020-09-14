from django.urls import path

from . import views

urlpatterns = [
    path("auth/cb/", views.client, name="Client"),
]
