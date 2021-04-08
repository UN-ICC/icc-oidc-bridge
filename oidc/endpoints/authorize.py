# from aca.client import ACAClient
from aries_cloudcontroller.aries_controller import AriesAgentController
from asgiref.sync import sync_to_async, async_to_sync
from django.utils import timezone
from datetime import timedelta

from aca.models import PresentationFactory
from oidc.utils.shortener import create_short_url
from oidc.models import AuthSession, PresentationConfigurations, MappedUrl
from django.conf import settings

WEBHOOK_HOST = " https://6f0420f94071.ngrok.io"
WEBHOOK_PORT = 443
WEBHOOK_BASE = " https://6f0420f94071.ngrok.io/webhooks/"


@async_to_sync
async def authorization(pres_req_conf_id: str, request_parameters: dict):
    # Based on the aca-py agent you wish to control
    print('BEFORE WEBHOOK START')
    agent_controller = AriesAgentController(admin_url=settings.ACA_PY_URL)
    print('ACAPY controller started')
    await agent_controller.init_webhook_server(webhook_host=WEBHOOK_HOST, webhook_port=WEBHOOK_PORT, webhook_base=WEBHOOK_BASE)
    print('WEBHOOOKS STARTED')
    presentation_configuration = PresentationConfigurations.objects.get(
        id=pres_req_conf_id
    )

    response = await agent_controller.proofs.create_request(presentation_configuration.to_json())
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print(response)
    public_did = await agent_controller.wallet.get_public_did()
    print(public_did)
    endpoint = await agent_controller.ledger.get_did_endpoint()
    print(endpoint)
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n\n\n\n\n\n')

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
