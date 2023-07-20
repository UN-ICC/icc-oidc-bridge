from django.urls import path

from . import views

urlpatterns = [
    path("webhooks/<str:api_key>/topic/<str:topic>/", views.webhooks, name="webhooks"),
    path("url/<str:key>", views.url_shortener, name="url_shortener"),
    path(
        "api/vc-configs/<str:pk>",
        views.PresentationConfigurationViews.as_view(),
        name="PresentationConfiguration",
    ),
    path("vc/connect/authorize/", views.authorize, name="authorize"),
    path("vc/connect/poll", views.poll, name="poll"),
    path("vc/connect/callback", views.callback, name="callback"),
    path("vc/connect/token", views.token_endpoint, name="token_endpoint"),
    path("", views.index, name="Index"),
]
