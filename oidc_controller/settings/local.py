import os

from oidc_controller.settings.base import *

ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.environ["SECRET_KEY"]

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
        "NAME": os.environ["OIDC_DB_NAME"],
        "USER": os.environ["OIDC_DB_USER"],
        "PASSWORD": os.environ["OIDC_DB_PASSWORD"],
        "HOST": "oidc-db",
        "PORT": os.environ["OIDC_DB_PORT"],
    }
}

ACA_PY_ADMIN_PORT = os.environ["ACAPY_ADMIN_PORT"]
ACA_PY_TRANSPORT_PORT = os.environ["ACAPY_TRANSPORT_PORT"]


SITE_URL = os.environ["SITE_URL"]

JWT_TOKEN_VALIDITY = 720
JWT_TOKEN_ISSUER = SITE_URL
JWT_KEY_KID = "3fd0079d2f87421708864ee9c84c8d4d"

#TODO extract API key and Webhooks to dockerfile
ACA_PY_WEBHOOK_HOST = "0.0.0.0"
ACA_PY_WEBHOOK_PORT = 8022
ACA_PY_WEBHOOK_BASE = ""
API_KEY = "alice_api_123456789"

ACA_PY_URL = f"http://aca-py:{ACA_PY_ADMIN_PORT}"
ACA_PY_TRANSPORT_URL = f"http://aca-py:{ACA_PY_TRANSPORT_PORT}"
POLL_INTERVAL = 5000
POLL_MAX_TRIES = 12
