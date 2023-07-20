import os

from distutils.util import strtobool

from oidc_controller.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = strtobool(os.environ.get("DEBUG", "True"))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*")

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = ["Content-type", "Accept", "Accept-Language", "Content-Language",
                      "Authorization"]
CSRF_TRUSTED_ORIGINS = ["*"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": os.environ.get("LOCATION", "default"),
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "oidc_controller"),
        "USER": os.environ.get("DB_USER", "oidc_controller"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "change_me"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", 5432),
    }
}

BASE_URL = os.environ.get("BASE_URL")
SITE_URL = os.environ.get("SITE_URL", f"https://{BASE_URL}")

JWT_KEY_KID = os.environ.get("JWT_KEY_KID")
JWT_TOKEN_ISSUER_PORT = os.environ.get("JWT_TOKEN_ISSUER_PORT", ":8080")
JWT_TOKEN_ISSUER = os.environ.get("SITE_URL", f"{BASE_URL}{JWT_TOKEN_ISSUER_PORT}")
JWT_TOKEN_VALIDITY = os.environ.get("JWT_TOKEN_VALIDITY", 720)

ACA_PY_BASE_URL = os.environ.get("ACA_PY_BASE_URL")
ACAPY_ADMIN_PORT = os.environ.get("ACAPY_ADMIN_PORT", 4001)
ACAPY_TRANSPORT_PORT = os.environ.get("ACAPY_TRANSPORT_PORT", 8100)
ACA_PY_URL = os.environ.get("ACA_PY_URL", f"https://{ACA_PY_BASE_URL}:{ACAPY_ADMIN_PORT}")
ACA_PY_TRANSPORT_URL = os.environ.get("ACA_PY_TRANSPORT_URL", f"https://{ACA_PY_BASE_URL}:{ACAPY_TRANSPORT_PORT}")

POLL_INTERVAL = os.environ.get("POLL_INTERVAL", 5000)
POLL_MAX_TRIES = os.environ.get("POLL_MAX_TRIES", 12)

SESSION_COOKIE_SECURE = strtobool(os.environ.get("SESSION_COOKIE_SECURE", "True"))
CSRF_COOKIE_SECURE = strtobool(os.environ.get("CSRF_COOKIE_SECURE", "True"))
SECURE_SSL_REDIRECT = strtobool(os.environ.get("SECURE_SSL_REDIRECT", "True"))
