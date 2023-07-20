import base64
import json


def encode_base64(payload: dict) -> str:
    return base64.b64encode(bytes(json.dumps(payload), "utf-8")).decode("utf-8")


def decode_base64(b64_input: str) -> dict:
    return json.loads(base64.b64decode(b64_input).decode("utf-8"))
