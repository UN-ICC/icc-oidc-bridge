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
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST":os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
    }
}

ACAPY_ADMIN_PORT = os.environ["ACAPY_ADMIN_PORT"]
ACAPY_TRANSPORT_PORT = os.environ["ACAPY_TRANSPORT_PORT"]


SITE_URL = os.environ["SITE_URL"]

JWT_TOKEN_VALIDITY = 720
JWT_TOKEN_ISSUER = SITE_URL
JWT_KEY_KID = os.environ.get("JWT_KEY_KID")

POLL_INTERVAL = 5000
POLL_MAX_TRIES = 12

ACA_PY_BASE_URL = os.environ.get("ACA_PY_BASE_URL")
ACAPY_ADMIN_PORT = os.environ.get("ACAPY_ADMIN_PORT", 4001)
ACAPY_TRANSPORT_PORT = os.environ.get("ACAPY_TRANSPORT_PORT", 8100)
ACA_PY_URL = os.environ.get("ACA_PY_URL", f"https://{ACA_PY_BASE_URL}:{ACAPY_ADMIN_PORT}")
ACA_PY_TRANSPORT_URL = os.environ.get(
    "ACA_PY_TRANSPORT_URL", f"https://{ACA_PY_BASE_URL}:{ACAPY_TRANSPORT_PORT}"
)
ACA_PY_WEBHOOKS_API_KEY = os.environ.get("ACA_PY_WEBHOOKS_API_KEY")
