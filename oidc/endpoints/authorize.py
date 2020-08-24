from aca.aca import ACAClient, Presentation
from django.utils import timezone
from datetime import timedelta
from oidc.utils.shortener import create_short_url
from oidc.models import AuthSession, PresentationConfigurations, MappedUrl
from django.conf import settings


def authorization(pres_req_conf_id: str, request_parameters: dict):
    aca_client = ACAClient(settings.ACA_PY_URL)
    presentation_configuration = PresentationConfigurations.objects.get(
        id=pres_req_conf_id
    )

    response = aca_client.create_proof_request(presentation_configuration.to_json())
    public_did = aca_client.get_public_did()
    endpoint = aca_client.get_endpoint_url()
    presentation_request = Presentation(
        presentation=response.get("presentation_request"),
        p_id=response.get("thread_id"),
        public_did=public_did,
        endpoint=endpoint,
    ).to_json()

    presentation_request_id = response["presentation_exchange_id"]
    session = AuthSession.objects.create(
        presentation_record_id=pres_req_conf_id,
        presentation_request_id=presentation_request_id,
        presentation_request=presentation_request,
        request_parameters=request_parameters,
        expired_timestamp=timezone.now() + timedelta(minutes=60),
    )
    url = create_short_url(presentation_request)
    mapped_url = MappedUrl.objects.create(url=url, session=session)
    short_url = mapped_url.get_short_url()

    return short_url, str(session.pk), presentation_request_id
