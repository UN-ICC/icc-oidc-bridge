# from aca.client import ACAClient
from aries_cloudcontroller.aries_controller import AriesAgentController
from django.utils import timezone
from datetime import timedelta

from aca.models import PresentationFactory
from oidc.utils.shortener import create_short_url
from oidc.models import AuthSession, PresentationConfigurations, MappedUrl
from django.conf import settings


def authorization(pres_req_conf_id: str, request_parameters: dict):
    #aca_client = ACAClient(settings.ACA_PY_URL, settings.ACA_PY_TRANSPORT_URL)
    # Based on the aca-py agent you wish to control
    agent_controller = AriesAgentController(admin_url=settings.ACA_PY_URL, api_key=API_KEY)
    presentation_configuration = PresentationConfigurations.objects.get(
        id=pres_req_conf_id
    )

    #response = aca_client.create_proof_request(presentation_configuration.to_json())
    response = agent_controller.proofs.create_request(presentation_configuration.to_json())
    # public_did = aca_client.get_public_did()
    public_did =  agent_controller.wallet.get_public_did()
    # endpoint = aca_client.get_endpoint_url()
    endpoint = agent_controller.ledger.get_did_endpoint()

    presentation_request = PresentationFactory.from_params(
        presentation_request=response.get("presentation_request"),
        p_id=response.get("thread_id"),
        verkey=[public_did.get("verkey")],
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
    url, b64_presentation = create_short_url(presentation_request)
    mapped_url = MappedUrl.objects.create(url=url, session=session)
    short_url = mapped_url.get_short_url()

    return short_url, str(session.pk), presentation_request_id, b64_presentation
