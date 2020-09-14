import pytest
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


@pytest.mark.django_db
class TestPresentationConfigurationViews:
    def test_without_credentials(self, api_client):
        response = api_client.post("/api/vc-configs/1", {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
