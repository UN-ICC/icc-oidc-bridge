import base64
import json

from django.conf import settings


def create_short_url(presentation_request: dict):
    b64_presentation = base64.b64encode(
        bytes(json.dumps(presentation_request), "utf-8")
    ).decode("utf-8")
    url = f"{settings.SITE_URL}?m={b64_presentation}"
    return url, b64_presentation
