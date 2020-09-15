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
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ0ZXN0QG1haWwub3JnIiwiYXVkIjoiYXVkaWVuY2UiLCJpc3MiOiJpc3N1ZXIiLCJpYXQiOjE1Nzc4MzY4MDAsIm5iZiI6MTU3NzgzNjgwMCwiZXhwIjoxNTc3ODM2ODYwfQ.dgsSlQSA11QPPmotQ8RPLCHm90_d9ScZD1LriMYYkQ6ajMbaLZtyaK3xsRs9rmADqqVafy0gaLYHIHTcxJm7SGZOaZJ03sUc2HStIOfV-ip-2deKKft3nVDYEN8VAjEn1srttUOexZv54TJJ-Qasf-8VU7Zc0XF5m8k17pReSWNISSnXRydCMi56YVkSvRHZ6SPxR7Fc0ngYFrgZm8vOjp0VHmBZvR0X347vrQJvRpYdNyzkwiuHHa1BM6K2-XE1O5qkDrKCvwfp3dCxS0VX7We9UC-3DeHQJzi-DfdPyXAykpibwy99swtVbowQ0Bwt_1NQKzCTQTqf_2aK2yPBbA"
        )

    @freeze_time("2020-01-01")
    def test_token_without_key(self):
        with pytest.raises(Exception):
            token(
                1, "issuer", "audience", {"sub": "test@mail.org"}, settings.JWT_KEY_KID
            )
