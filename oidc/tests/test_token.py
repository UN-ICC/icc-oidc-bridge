import pytest
from django.core.exceptions import ObjectDoesNotExist
from oidc.endpoints.token import create_id_token, extract_claims
from oidc.utils.token import token
from django.utils import timezone
import uuid
from freezegun import freeze_time
from django.conf import settings


@pytest.mark.django_db
class TestTokenEndpoint:
    def test_extract_claims_with_email_as_sub(
        self, mocker, validated_session, email_presentation_configuration
    ):
        mocker.patch.object(timezone, "now", return_value=1)
        claims = extract_claims(validated_session)
        assert claims == {
            "acr": "vc_authn",
            "email": "test@mail.org",
            "iat": 1,
            "nonce": "vdoOCIrMvSRn2vYcgAV3vszUKb3ACJlD",
            "pres_req_conf_id": "e2e1b664-5fd9-401d-96bc-26a62c4777a8",
            "sub": "test@mail.org",
        }

    def test_extract_claims_without_sub(
        self, mocker, validated_session, name_presentation_configuration
    ):
        mocker.patch.object(timezone, "now", return_value=1)
        mocker.patch.object(uuid, "uuid4", return_value=1)
        claims = extract_claims(validated_session)
        assert claims == {
            "acr": "vc_authn",
            "email": "test@mail.org",
            "iat": 1,
            "nonce": "vdoOCIrMvSRn2vYcgAV3vszUKb3ACJlD",
            "pres_req_conf_id": "e2e1b664-5fd9-401d-96bc-26a62c4777a8",
            "sub": "1",
        }

    def test_extract_claims__without_presentation_configuratio(
        self, mocker, validated_session
    ):
        with pytest.raises(Exception):
            extract_claims(validated_session)

    def test_create_token(self, mocker, jwt_key, validated_session):
        claims = {
            "acr": "vc_authn",
            "email": "test@mail.org",
            "iat": 1,
            "nonce": "vdoOCIrMvSRn2vYcgAV3vszUKb3ACJlD",
            "pres_req_conf_id": "e2e1b664-5fd9-401d-96bc-26a62c4777a8",
            "sub": "test@mail.org",
        }
        mocker.patch("oidc.endpoints.token.extract_claims", return_value=claims)
        token_mock = mocker.patch("oidc.endpoints.token.token", return_value="token")
        token = create_id_token(validated_session)

        assert token == "token"
        token_mock.assert_called_with(
            settings.JWT_TOKEN_VALIDITY,
            "http://127.0.0.1",
            "770241",
            claims,
            settings.JWT_KEY_KID,
        )


@pytest.mark.django_db
class TestTokenUtils:
    @freeze_time("2020-01-01")
    def test_token(self, jwt_key):
        tk = token(
            1, "issuer", "audience", {"sub": "test@mail.org"}, settings.JWT_KEY_KID
        )
        assert (
            tk
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjNlM2VlM2Y3NjdhODNkMTZmM2NlZTAyZWI1ZTVlYjkyIn0.eyJzdWIiOiJ0ZXN0QG1haWwub3JnIiwiYXVkIjoiYXVkaWVuY2UiLCJpc3MiOiJpc3N1ZXIiLCJpYXQiOjE1Nzc4MzY4MDAsIm5iZiI6MTU3NzgzNjgwMCwiZXhwIjoxNTc3ODM2ODYwfQ.LXn27zNszxXR1udM1L-4tsJNeyety0GCVj-6prTrtRa-xQxQmsk-lvHdwj7CLeyCdgPdSplqEqx63UF83WNjibs-rulXZ1M8BKkvF8lCroLju4d1byRDK-M4Au5GHvN4nt1PdBc4ik_04tW8Ylr-lv64d9pzeaICuAf3B-7QQBF2A2S83wncKPUM4Y34lS4NzHrP_djuR1kip6mDQs-9zvvm_oQZfy6KBTwV7THDI90TCtzqoQdT0_gj-oxNEyGgT-CtaPR6gLyo_Xl4w_agM3sCQPuqLYwhF2c8NWlRGqycsyXRITNBp6ESrHQHU68hKgqyHrJ7XLUDGhaNn5L5RA"
        )

    @freeze_time("2020-01-01")
    def test_token_without_key(self):
        with pytest.raises(Exception):
            token(
                1, "issuer", "audience", {"sub": "test@mail.org"}, settings.JWT_KEY_KID
            )
