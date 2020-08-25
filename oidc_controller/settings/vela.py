import os

from oidc_controller.settings.base import *

ALLOWED_HOSTS = ["*"]

DEBUG = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default",
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "oidc_controller",
        "USER": "oidc_controller",
        "PASSWORD": "&^6ergsdfdH7d",
        "HOST": "127.0.0.1",
        "PORT": 5432,
    }
}

SITE_URL = "http://10.90.46.61:8080"

JWT_TOKEN_VALIDITY = 720
JWT_TOKEN_ISSUER = "10.90.46.61:8080"
JWT_KEY_KID = "3e3ee3f767a83d16f3cee02eb5e5eb92"

ACA_PY_URL = "http://10.90.46.61:4000"
POLL_INTERVAL = 5000
POLL_MAX_TRIES = 12
