import requests
import base64
import json


def encode_base64(payload: dict) -> str:
    return base64.b64encode(bytes(json.dumps(payload), "utf-8")).decode("utf-8")


def decode_base64(payload: str) -> dict:
    return json.loads(base64.b64decode(payload).decode("utf-8"))


class Presentation:
    @classmethod
    def __init__(
        self,
        presentation: dict,
        p_id: str,
        public_did: str,
        endpoint: str,
        p_type: str = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
        routing_keys: str = None,
    ):
        self.presentation = presentation
        self.p_id = p_id
        self.p_type = p_type
        self.public_did = public_did
        self.endpoint = endpoint
        self.routing_keys = routing_keys

    @classmethod
    def from_didcom(cls, presentation_request: dict):
        presentation = (
            presentation_request.get("request_presentations~attach", {})
            .get("data", {})
            .get("base64", "")
        )

        service = presentation_request.get("~service", {})
        return cls(
            presentation=decode_base64(presentation),
            p_id=presentation_request.get("@id"),
            p_type=presentation_request.get("@type"),
            public_did=service.get("recipientKeys"),
            endpoint=service.get("serviceEndpoint"),
            routing_keys=service.get("routingKeys"),
        )

    def to_json(self):
        return {
            "@id": self.p_id,
            "@type": self.p_type,
            "request_presentations~attach": {
                "@id": "libindy-request-presentation-0",
                "mime-type": "application/json",
                "data": {"base64": encode_base64(self.presentation)},
            },
            "~service": {
                "recipientKeys": [self.public_did],
                "routingKeys": self.routing_keys,
                "serviceEndpoint": self.endpoint,
            },
        }


class ACAClient:
    def __init__(self, url: str, token: str = None) -> None:
        self.url = url
        self.token = token

        headers = {"accept": "application/json", "Content-Type": "application/json"}
        if self.token:
            headers.update({"X-API-Key": f"{self.token}"})

        self.session = requests.Session()
        self.session.headers.update(headers)

    def create_proof_request(self, presentation_request: dict) -> dict:
        response = self.session.post(
            f"{self.url}/present-proof/create-request", json=presentation_request
        )
        response.raise_for_status()
        return response.json()

    def get_public_did(self) -> list:
        response = self.session.get(f"{self.url}/wallet/did/public")
        response.raise_for_status()
        return response.json()["result"]

    def get_endpoint_url(self):
        return self.url
