from .base import *

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

JWT_TOKEN_VALIDITY = 1
JWT_KEY_KID = "3e3ee3f767a83d16f3cee02eb5e5eb92"
JWT_TOKEN_ISSUER = "http://127.0.0.1"
