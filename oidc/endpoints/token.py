from oidc.models import PresentationConfigurations, AuthSession
from django.conf import settings
from django.utils import timezone
from oidc.utils.token import token
import uuid
from aca.aca import PresentationFactory


def create_id_token(session: AuthSession):
    IDENTITY_PARAM = "sub"

    audience = session.request_parameters.get("client_id", "")
    presentation_configuration = PresentationConfigurations.objects.filter(
        id=session.presentation_record_id
    ).last()
    nonce = session.request_parameters.get("nonce")
    issuer = settings.JWT_TOKEN_ISSUER

    claims = {"pres_req_conf_id": session.presentation_request_id, "acr": "vc_authn"}

    if nonce:
        claims.update({"nonce": nonce})

    presentation = PresentationFactory.from_json(session.presentation_request)
    requested_parameters = presentation.presentation.__dict__

    if isinstance(requested_parameters, dict):
        for k, v in requested_parameters.get("requested_attributes", {}).items():
            attr = (
                session.presentation.get("requested_proof", {})
                .get("revealed_attributes", {})
                .get(k)
            )
            if attr:
                claims.update({v: attr.get("raw", "")})
                if (
                    presentation_configuration
                    and presentation_configuration.subject_identifier == v
                ):
                    claims.update({IDENTITY_PARAM: attr.get("raw", "")})

    if IDENTITY_PARAM not in claims.keys():
        claims.update({IDENTITY_PARAM: str(uuid.uuid4())})

    claims.update({"iat": timezone.now()})

    return token(
        settings.JWT_TOKEN_VALIDITY, issuer, audience, claims, settings.JWT_KEY_KID
    )
