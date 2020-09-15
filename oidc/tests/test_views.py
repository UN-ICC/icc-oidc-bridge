import json
import uuid

import pytest
from django.test import override_settings
from oidc_provider.lib.endpoints.authorize import AuthorizeEndpoint
from oidc_provider.lib.errors import AuthorizeError
from rest_framework import status

from oidc.models import PresentationConfigurations, AuthSession


class TestIndex:
    def test_index(self, api_client):
        assert api_client.get("/").status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPresentationConfigurationViews:
    def test_without_credentials(self, api_client):
        response = api_client.post("/api/vc-configs/1", {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve(self, api_client_admin, email_presentation_configuration):
        response = api_client_admin.get(
            f"/api/vc-configs/{email_presentation_configuration.id}"
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update(self, api_client_admin, email_presentation_configuration):
        response = api_client_admin.patch(
            f"/api/vc-configs/{email_presentation_configuration.id}",
            {"subject_identifier": "new_subject"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["subject_identifier"] == "new_subject"

    def test_delete(self, api_client_admin, email_presentation_configuration):
        response = api_client_admin.delete(
            f"/api/vc-configs/{email_presentation_configuration.id}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(PresentationConfigurations.objects.all()) == 0


@pytest.mark.django_db
class TestWebhooks:
    def test_unknown_topic(self, api_client, non_validated_session):
        response = api_client.post(
            f"/webhooks/topic/unknown_topic/",
            data=json.dumps({"state": "presentation_received"}),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert AuthSession.objects.first().presentation_request_satisfied is False

    def test_present_proof_presentation_not_received(
        self, api_client, non_validated_session
    ):
        response = api_client.post(
            f"/webhooks/topic/present_proof/",
            data=json.dumps({"state": "some_state"}),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert AuthSession.objects.first().presentation_request_satisfied is False

    def test_present_proof_wrong_body(self, api_client, non_validated_session):
        response = api_client.post(
            f"/webhooks/topic/present_proof/",
            data=json.dumps({"state": "presentation_received"}),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert AuthSession.objects.first().presentation_request_satisfied is False

    def test_present_proof_session_not_found(self, api_client, non_validated_session):
        response = api_client.post(
            f"/webhooks/topic/present_proof/",
            data=json.dumps(
                {
                    "state": "presentation_received",
                    "presentation": {"requested_proof": "req_proof"},
                    "presentation_exchange_id": "unknown_pres_id",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert AuthSession.objects.first().presentation_request_satisfied is False

    def test_present_proof_session_satisfied(self, api_client, non_validated_session):
        response = api_client.post(
            f"/webhooks/topic/present_proof/",
            data=json.dumps(
                {
                    "state": "presentation_received",
                    "presentation": {"requested_proof": {"proof": "req_proof"}},
                    "presentation_exchange_id": non_validated_session.presentation_request_id,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert AuthSession.objects.first().presentation_request_satisfied is True


@pytest.mark.django_db
class TestUrlShortener:
    def test_wrong_key(self, api_client):
        response = api_client.get("/url/unknown_key")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_ok(self, api_client, mapped_url):
        response = api_client.get(f"/url/{mapped_url.id}")
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == mapped_url.url


@pytest.mark.django_db
class TestPoll:
    def test_wrong_presentation_id(self, api_client):
        response = api_client.get("/vc/connect/poll")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = api_client.get("/vc/connect/poll?pid=unknown")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_session_not_satisfied(self, api_client, non_validated_session):
        response = api_client.get(
            f"/vc/connect/poll?pid={non_validated_session.presentation_request_id}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_session_satisfied(self, api_client, validated_session):
        response = api_client.get(
            f"/vc/connect/poll?pid={validated_session.presentation_request_id}"
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCallback:
    def test_wrong_presentation_id(self, api_client):
        response = api_client.get("/vc/connect/callback")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = api_client.get("/vc/connect/callback?pid=unknown")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_session_not_satisfied(self, api_client, non_validated_session):
        response = api_client.get(
            f"/vc/connect/callback?pid={non_validated_session.presentation_request_id}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_response_type_not_code(self, api_client, validated_session):
        validated_session.request_parameters = {
            "state": "some_state",
            "redirect_uri": "https://redirect.com",
            "response_type": "not_code",
        }
        validated_session.save()
        response = api_client.get(
            f"/vc/connect/callback?pid={validated_session.presentation_request_id}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client.get(
            f"/vc/connect/callback?pid={validated_session.presentation_request_id}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_ok(self, api_client, validated_session):
        response = api_client.get(
            f"/vc/connect/callback?pid={validated_session.presentation_request_id}"
        )
        assert response.status_code == status.HTTP_302_FOUND
        assert (
            response.url
            == f"{validated_session.request_parameters.get('redirect_uri')}"
            f"?code={validated_session.pk}"
            f"&state={validated_session.request_parameters.get('state')}"
        )


@pytest.mark.django_db
class TestTokenEndpoint:
    def test_wrong_grant_type(self, api_client):
        response = api_client.post(
            "/vc/connect/token", data=json.dumps({}), content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client.post(
            "/vc/connect/token",
            data=json.dumps({"grant_type": "unknown_type"}),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_wrong_code(self, api_client):
        response = api_client.post(
            "/vc/connect/token",
            data=json.dumps({"grant_type": "authorization_code"}),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client.post(
            "/vc/connect/token",
            data=json.dumps(
                {"grant_type": "authorization_code", "code": str(uuid.uuid4())}
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_session_not_satisfied(self, api_client, non_validated_session):
        response = api_client.post(
            f"/vc/connect/token",
            data=json.dumps(
                {
                    "grant_type": "authorization_code",
                    "code": str(non_validated_session.pk),
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_session_ok(self, mocker, api_client, validated_session):
        create_id_token = mocker.patch(
            "oidc.views.create_id_token", return_value="id_token"
        )

        response = api_client.post(
            f"/vc/connect/token",
            data=json.dumps(
                {"grant_type": "authorization_code", "code": str(validated_session.pk),}
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        response_content = response.json()
        assert response_content == {
            "access_token": "invalid",
            "id_token": "id_token",
            "token_type": "Bearer",
        }
        assert not AuthSession.objects.filter(id=validated_session.id).all()
        create_id_token.assert_called_once()


@pytest.mark.django_db
class TestAuthorize:
    def test_without_pres_req_conf_id(self, api_client):
        response = api_client.get("/vc/connect/authorize/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_wrong_scope(self, api_client):
        response = api_client.get("/vc/connect/authorize/?pres_req_conf_id=pid")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client.get(
            "/vc/connect/authorize/?pres_req_conf_id=pid&scope=unknown"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client.get(
            "/vc/connect/authorize/?pres_req_conf_id=pid&scope=unknown unknown2"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_params(self, mocker, api_client):
        mocker.patch.object(AuthorizeEndpoint, "__init__", return_value=None)
        mocker.patch.object(
            AuthorizeEndpoint,
            "validate_params",
            side_effect=AuthorizeError("err", "desc", "grant_type"),
        )

        response = api_client.get(
            "/vc/connect/authorize/?pres_req_conf_id=pid&scope=some_scope vc_authn"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @override_settings(
        SITE_URL="http://site.com", POLL_INTERVAL=5000, POLL_MAX_TRIES=10
    )
    def test_ok(self, mocker, api_client):
        mocker.patch.object(AuthorizeEndpoint, "__init__", return_value=None)
        mocker.patch.object(
            AuthorizeEndpoint, "validate_params", return_value=True,
        )
        mocker.patch(
            "oidc.views.authorization",
            return_value=(
                "http://short-url.com",
                "ses_id",
                {"presentation": "request"},
                "1234abcd",
            ),
        )

        response = api_client.get(
            "/vc/connect/authorize/?pres_req_conf_id=pid&scope=some_scope vc_authn"
        )
        assert response.status_code == status.HTTP_200_OK
