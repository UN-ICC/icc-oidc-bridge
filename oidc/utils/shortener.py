import base64
import json


def create_short_url(presentation_request: dict):
    b64_presentation = base64.b64encode(
        bytes(json.dumps(presentation_request), "utf-8")
    ).decode("utf-8")
    url = f"http://10.90.46.61:8080?m={b64_presentation}"
    return url
