from unittest.mock import MagicMock

import pytest
import requests
from django.test import override_settings
from rest_framework import status


@pytest.mark.django_db
class TestClient:
    def test_without_code(self, api_client):
        response = api_client.post("/oidc/auth/cb/", {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @override_settings(SITE_URL="https://site.com")
    def test_bad_token_response(self, mocker, api_client):
        token_response = MagicMock()
        token_response.json.side_effect = Exception()
        token_request = mocker.patch.object(
            requests, "post", return_value=token_response
        )

        response = api_client.get("/oidc/auth/cb/?code=1234")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        token_request.assert_called_once_with(
            "https://site.com/vc/connect/token",
            json={"code": "1234", "grant_type": "authorization_code"},
        )
        token_response.raise_for_status.assert_called_once()
        token_response.json.assert_called_once()

    @override_settings(SITE_URL="https://site.com")
    def test_ok(self, mocker, api_client):
        token_response = MagicMock()
        token_response.json.return_value = {"id_token": "my_token"}
        token_request = mocker.patch.object(
            requests, "post", return_value=token_response
        )

        response = api_client.get("/oidc/auth/cb/?code=1234")

        assert response.status_code == status.HTTP_200_OK
        token_request.assert_called_once_with(
            "https://site.com/vc/connect/token",
            json={"code": "1234", "grant_type": "authorization_code"},
        )
        token_response.raise_for_status.assert_called_once()
        token_response.json.assert_called_once()
