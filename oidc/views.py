import json
import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseNotFound,
    JsonResponse,
    HttpResponseServerError,
    HttpResponseForbidden,
)
from oidc_provider.lib.utils.common import cors_allow_any
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from oidc.serializers import PresentationConfigurationSerializer
from oidc.endpoints.token import create_id_token
from oidc.endpoints.authorize import authorization
from oidc.models import MappedUrl, AuthSession, PresentationConfigurations
from oidc_provider.lib.endpoints.authorize import AuthorizeEndpoint

LOGGER = logging.getLogger(__name__)


class PresentationConfigurationViews(RetrieveUpdateDestroyAPIView):
    serializer_class = PresentationConfigurationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PresentationConfigurations.objects.all()


def index(request):
    return HttpResponse()


@csrf_exempt
def webhooks(request, api_key, topic):
    if api_key != settings.ACA_PY_WEBHOOKS_API_KEY:
        LOGGER.error(f"Unauthorized webhook {topic} 'ACA_PY_WEBHOOKS_API_KEY' is not valid")
        return HttpResponse()

    message = json.loads(request.body)

    LOGGER.info(f"webhook received - topic: {topic} and message: {message}")
    # Should be triggered after a proof request has been sent by the org
    if topic == "present_proof":
        state = message["state"]
        if state != "presentation_received":
            LOGGER.info(f"Presentation Request not yet received, state is [{state}]")
            return HttpResponse()

        presentation_exchange_id = "- not_set -"
        try:
            proof = message["presentation"]["requested_proof"]
            presentation_exchange_id = message["presentation_exchange_id"]

            LOGGER.info(f"Proof received: {proof}")

            session = AuthSession.objects.get(presentation_request_id=presentation_exchange_id)
            session.satisfy_session(proof)

        except (AuthSession.DoesNotExist, AuthSession.MultipleObjectsReturned):
            LOGGER.warning(
                f"Could not find a corresponding auth session to satisfy. "
                f"Presentation request id: [{presentation_exchange_id}]"
            )
            return HttpResponse()

        except Exception as e:
            LOGGER.error(f"Wrong 'present_proof' body: {message} - error: {e}")
            return HttpResponse()

    return HttpResponse()


def url_shortener(request, key: str):
    if request.method == "GET":
        try:
            mapped_url = MappedUrl.objects.get(id=key)
            return HttpResponseRedirect(mapped_url.url)
        except Exception:
            return HttpResponseBadRequest("Wrong key provided")


def poll(request):
    if request.method == "GET":
        presentation_request_id = request.GET.get("pid")
        if not presentation_request_id:
            return HttpResponseNotFound()

        session = get_object_or_404(AuthSession, presentation_request_id=presentation_request_id)

        if not session.presentation_request_satisfied:
            return HttpResponseBadRequest()

        return HttpResponse()


def callback(request):
    if request.method == "GET":
        presentation_request_id = request.GET.get("pid")
        if not presentation_request_id:
            return HttpResponseNotFound()

        session = get_object_or_404(AuthSession, presentation_request_id=presentation_request_id)

        if not session.presentation_request_satisfied:
            return HttpResponseForbidden()

        if session.request_parameters.get("response_type", "") == "code":
            redirect_uri = session.request_parameters.get("redirect_uri", "")
            url = f"{redirect_uri}?code={session.pk}"
            state = session.request_parameters.get("state")
            if state:
                url += f"&state={state}"
            LOGGER.info(f"Callback: Redirecting to {url}")

            redirect = request.GET.get("redirect")
            if redirect and redirect == "false":
                return JsonResponse({"url": url})

            return HttpResponseRedirect(url)

        return HttpResponseBadRequest()


@csrf_exempt
def token_endpoint(request):

    def set_headers(response):
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        cors_allow_any(request, response)
        return response

    if request.method == "OPTIONS":
        return set_headers(HttpResponse())

    if request.method == "POST":
        try:
            message = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            message = request.POST.dict()
        grant_type = message.get("grant_type")
        if not grant_type or grant_type != "authorization_code":
            return HttpResponseBadRequest()

        session_id = message.get("code")
        if not session_id:
            return HttpResponseBadRequest()

        session = get_object_or_404(AuthSession, id=session_id)

        if not session.presentation_request_satisfied:
            return HttpResponseBadRequest()

        try:
            token = create_id_token(session)
            session.delete()
        except Exception as e:
            LOGGER.warning(f"Error creating token for {session_id}: {e}")
            return HttpResponseServerError()

        data = {"access_token": "invalid", "id_token": token, "token_type": "Bearer"}
        success_response = JsonResponse(data, status=200)
        set_headers(success_response)

        return success_response


def authorize(request):
    template_name = "qr_display.html"

    if request.method == "GET":
        pres_req_conf_id = request.GET.get("pres_req_conf_id")
        if not pres_req_conf_id:
            return HttpResponseBadRequest("pres_req_conf_id query parameter not found")

        scopes = request.GET.get("scope")
        if not scopes or "vc_authn" not in scopes.split(" "):
            return HttpResponseBadRequest("Scope vc_authn not found")

        aut = AuthorizeEndpoint(request)
        try:
            aut.validate_params()
        except Exception as e:
            return HttpResponseBadRequest(
                f"Error validating parameters: [{e.error}: {e.description}]"
            )

        short_url, session_id, pres_req, b64_presentation = authorization(
            pres_req_conf_id, request.GET
        )
        request.session["sessionid"] = session_id

        response = {
            "url": short_url,
            "b64_presentation": b64_presentation,
            "poll_interval": settings.POLL_INTERVAL,
            "poll_max_tries": settings.POLL_MAX_TRIES,
            "poll_url": f"{settings.SITE_URL}/vc/connect/poll?pid={pres_req}",
            "resolution_url": f"{settings.SITE_URL}/vc/connect/callback?pid={pres_req}",
        }

        # If prompt=none just return data as JSON
        prompt = request.GET.get("prompt", "")
        if prompt == "none":
            return JsonResponse(response)

        return TemplateResponse(
            request,
            template_name,
            response,
        )
