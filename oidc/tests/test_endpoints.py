from unittest.mock import ANY

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import URLValidator
from django.test import override_settings

from aca.aca import ACAClient
from oidc.endpoints.authorize import authorization
from oidc.models import AuthSession


@pytest.mark.django_db
class TestAuthorization:
    @override_settings(
        ACA_PY_URL="https://aca.com",
        ACA_PY_TRANSPORT_URL="https://aca-trans.com",
        SITE_URL="https://site.com",
    )
    def test_authorization_not_found(self, mocker, email_presentation_configuration):
        with pytest.raises(ObjectDoesNotExist):
            authorization("invalid_pres_req_conf_id", {})

    @override_settings(
        ACA_PY_URL="https://aca.com",
        ACA_PY_TRANSPORT_URL="https://aca-trans.com",
        SITE_URL="https://site.com",
    )
    def test_authorization(self, mocker, email_presentation_configuration):
        create_proof_req = mocker.patch.object(
            ACAClient,
            "create_proof_request",
            return_value={
                "presentation_request": "some_pr",
                "thread_id": "some_tid",
                "presentation_exchange_id": "some_pres_ex_id",
            },
        )
        get_public_did = mocker.patch.object(
            ACAClient, "get_public_did", return_value={"verkey": "some_verkey"}
        )

        short_url, session_id, pres_req, b64_presentation = authorization(
            "verified-email", {"some_param": "some_value"}
        )

        url_validator = URLValidator()
        url_validator(short_url)

        session = AuthSession.objects.first()
        assert session_id == str(session.id)
        assert session.presentation_record_id == "verified-email"
        assert session.presentation_request_id == "some_pres_ex_id"
        assert session.presentation_request == {
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
            "@id": "some_tid",
            "request_presentations~attach": [
                {
                    "@id": "libindy-request-presentation-0",
                    "data": {"base64": ANY},
                    "mime-type": "application/json",
                }
            ],
            "~service": {
                "serviceEndpoint": "https://aca-trans.com",
                "routingKeys": None,
                "recipientKeys": ["some_verkey"],
            },
            "comment": None,
        }
        assert session.request_parameters == {"some_param": "some_value"}
        assert pres_req == "some_pres_ex_id"
        assert b64_presentation
        create_proof_req.assert_called_once()
        get_public_did.assert_called_once()
