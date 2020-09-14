import logging

import requests
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.template.response import TemplateResponse

LOGGER = logging.getLogger(__name__)


def client(request):
    template_name = "token_result.html"

    LOGGER.info(f"Hit client with {request.GET}")

    code = request.GET.get("code")
    if not code:
        return HttpResponseBadRequest("Parameter 'code' not found")

    body = {"grant_type": "authorization_code", "code": code}

    LOGGER.info(f"Request token with: {body}")
    response = requests.post(f"{settings.SITE_URL}/vc/connect/token", json=body)
    response.raise_for_status()

    try:
        response_content = response.json()
        LOGGER.info(f"Request token response: {response_content}")
        return TemplateResponse(request, template_name, response_content)
    except Exception as e:
        LOGGER.error(f"Invalid token response: {e}")
        return HttpResponseBadRequest(f"Invalid token response: {e}")
