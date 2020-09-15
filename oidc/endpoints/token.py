from oidc.models import PresentationConfigurations, AuthSession
from django.conf import settings
from django.utils import timezone
from oidc.utils.token import token
import uuid
from aca.aca import PresentationFactory


def extract_claims(session: AuthSession):
    IDENTITY_PARAM = "sub"

    presentation_configuration = PresentationConfigurations.objects.filter(
        id=session.presentation_record_id
    ).last()

    if not presentation_configuration:
        raise Exception(
            "Presenstation configuraton not found with id: {session.presentation_record_id}"
        )
    nonce = session.request_parameters.get("nonce")

    claims = {"pres_req_conf_id": session.presentation_request_id, "acr": "vc_authn"}

    if nonce:
        claims.update({"nonce": nonce})

    presentation_factory = PresentationFactory.from_json(session.presentation_request)
    requested_parameters = presentation_factory.presentation.presentation

    if requested_parameters:
        for requested_attr in requested_parameters:
            for k, v in requested_attr.data.get("requested_attributes", {}).items():
                attr = session.presentation.get("revealed_attrs", {}).get(k)
                if attr:
                    attr_name = v.get("name")
                    claims.update({attr_name: attr.get("raw", "")})
                    if (
                        presentation_configuration
                        and presentation_configuration.subject_identifier == attr_name
                    ):
                        claims.update({IDENTITY_PARAM: attr.get("raw", "")})

    if IDENTITY_PARAM not in claims.keys():
        claims.update({IDENTITY_PARAM: str(uuid.uuid4())})

    claims.update({"iat": timezone.now()})

    return claims


def create_id_token(session: AuthSession):
    audience = session.request_parameters.get("client_id", "")
    issuer = settings.JWT_TOKEN_ISSUER
    claims = extract_claims(session)

    return token(
        settings.JWT_TOKEN_VALIDITY, issuer, audience, claims, settings.JWT_KEY_KID
    )
