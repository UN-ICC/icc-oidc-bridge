from aca.client import ACAClient
from aries_cloudcontroller.aries_controller import AriesAgentController
from asgiref.sync import sync_to_async, async_to_sync
from django.utils import timezone
from datetime import timedelta

from aca.models import PresentationFactory
from oidc.utils.shortener import create_short_url
from oidc.models import AuthSession, PresentationConfigurations, MappedUrl
from django.conf import settings
from datetime import datetime, timedelta

import asyncio

WEBHOOK_HOST = "https://8b1dec9d51dd.ngrok.io"
WEBHOOK_PORT = 443
WEBHOOK_BASE = "https://8b1dec9d51dd.ngrok.io/webhooks/"

def authorization(pres_req_conf_id: str, request_parameters: dict):
    aca_client = ACAClient(settings.ACA_PY_URL, settings.ACA_PY_TRANSPORT_URL)
    presentation_configuration = PresentationConfigurations.objects.get(
        id=pres_req_conf_id
    )

    response = aca_client.create_proof_request(presentation_configuration.to_json())
    print('PROOF CREATE', response)
    public_did = aca_client.get_public_did()
    print('DID', public_did)
    endpoint = aca_client.get_endpoint_url()
    print('ENDPOINT', endpoint)

    presentation_request = PresentationFactory.from_params(
        presentation_request=response.get("presentation_request"),
        p_id=response.get("thread_id"),
        verkey=[public_did.get("verkey")],
        endpoint=endpoint,
    ).to_json()

    print('PROOF REQUEST ', presentation_request)

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

@sync_to_async
def getPresentationConfig(pres_req_conf_id: str):
    return PresentationConfigurations.objects.get(
        id=pres_req_conf_id
    )
@sync_to_async
def createSession(pres_req_conf_id, presentation_request_id, presentation_request, request_parameters, url):
    session = AuthSession.objects.create(
        presentation_record_id=pres_req_conf_id,
        presentation_request_id=presentation_request_id,
        presentation_request=presentation_request,
        request_parameters=request_parameters,
        expired_timestamp= timezone.now() + timedelta(minutes=60),
    )
    mapped_url = MappedUrl.objects.create(url=url, session=session)
    print(mapped_url)
    short_url = mapped_url.get_short_url()
    print(short_url)

    return session, mapped_url, short_url

async def authorization_async(pres_req_conf_id: str, request_parameters: dict):
    # Based on the aca-py agent you wish to control
    # print('AGENT CONNECT')
    agent_controller = AriesAgentController(admin_url=settings.ACA_PY_URL)
    # print('ACAPY AGENT CONNECTED')
    # print('WEBHOOOKS STARTING')
    # await asyncio.gather(agent_controller.init_webhook_server(webhook_host=WEBHOOK_HOST, webhook_port=WEBHOOK_PORT, webhook_base=WEBHOOK_BASE))
    # print('WEBHOOOKS STARTED')
    presentation_configuration = await getPresentationConfig(pres_req_conf_id)
    print('PRESENTATION CONFIG: ', presentation_configuration)

    # response = await agent_controller.proofs.create_request(presentation_configuration.to_json())
    response = await asyncio.gather(agent_controller.proofs.create_request(presentation_configuration.to_json()))
    response = response[0]

    print('PROOF CREATE: ', response)
    # TODO - the current DID of the Agent is already ledgered on Stagingnet
    # This creates a scenario where the endpoint being fetched is wrong
    # Need to update the code so that new DIDs can be ledgered to stagingnet together with endpoints
    public_did = await asyncio.gather(agent_controller.wallet.get_public_did())
    public_did = public_did[0]['result']
    print('PUBLIC DID: ', public_did)
    endpoint = await asyncio.gather(agent_controller.ledger.get_did_endpoint(public_did['did']))
    endpoint = endpoint[0]['endpoint']
    print('ENDPOINT: ', endpoint)
    # TODO - this will wail due to no TAA accepted on ledger
    TAA_response = await agent_controller.ledger.get_taa()
    TAA = TAA_response['result']['taa_record']
    TAA['mechanism'] = "service_agreement"
    # print(TAA)

    TAA_accept = await agent_controller.ledger.accept_taa(TAA)
    ## Will return {} if successful
    print(TAA_accept)
    await asyncio.gather(agent_controller.wallet.set_did_endpoint(public_did['did'], settings.ACA_PY_TRANSPORT_URL, 'Endpoint'))
    endpoint = await asyncio.gather(agent_controller.ledger.get_did_endpoint(public_did['did']))
    endpoint = endpoint[0]['endpoint']
    print('ENDPOINT ', endpoint)
    presentation_request = PresentationFactory.from_params(
        presentation_request=response.get("presentation_request"),
        p_id=response.get("thread_id"),
        verkey=[public_did.get("verkey")],
        endpoint=endpoint,
    ).to_json()

    print('PROOF REQUEST: ', presentation_request)

    presentation_request_id = response["presentation_exchange_id"]

    url, b64_presentation = create_short_url(presentation_request)
    print(url)

    session, mapped_url, short_url = await createSession(pres_req_conf_id, presentation_request_id, presentation_request, request_parameters, url)

    print('SESSION ', session)
    print('sessionpk: ', str(session.pk))
    print('mapped_url: ', mapped_url)
    print('short_url: ', short_url)
    print('presx_id: ', presentation_request_id)
    print('b64 presx: ', b64_presentation)

    await agent_controller.terminate()
    return short_url, str(session.pk), presentation_request_id, b64_presentation

