import base64
import json

from django.conf import settings


def to_b64(content):
    return base64.b64encode(bytes(json.dumps(content), "utf-8")).decode("utf-8")


def create_short_url(presentation_request: dict):
    b64_presentation = to_b64(presentation_request)
    url = f"{settings.SITE_URL}?m={b64_presentation}"
    return url, b64_presentation
