import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    user = User.objects.create(username="admin", email="admin@unicc.org")
    return user


@pytest.fixture
def api_client_admin(admin_user):
    api_client = APIClient()
    token = Token.objects.create(user=admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {str(token)}")
    return api_client
