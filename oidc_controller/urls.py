"""oidc_controller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls import url

schema_view = get_schema_view(
    openapi.Info(
        title="OIDC API",
        default_version="v1",
        description="REST API definition for OIDC Controller",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("admin/", admin.site.urls),
    url(r"^openid/", include("oidc_provider.urls", namespace="oidc_provider")),
    path("oidc/", include("client.urls")),
    path("", include("oidc.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
