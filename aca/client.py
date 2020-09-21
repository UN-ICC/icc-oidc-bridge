import requests


class ACAClient:
    def __init__(self, url: str, transport_url: str, token: str = None) -> None:
        self.url = url
        self.transport_url = transport_url
        self.token = token

        headers = {"accept": "application/json", "Content-Type": "application/json"}
        if self.token:
            headers.update({"X-API-Key": f"{self.token}"})

        self.session = requests.Session()
        self.session.headers.update(headers)

    def get_endpoint_url(self):
        return self.transport_url

    def create_proof_request(self, presentation_request: dict) -> dict:
        response = self.session.post(
            f"{self.url}/present-proof/create-request", json=presentation_request
        )
        response.raise_for_status()
        return response.json()

    def get_public_did(self) -> dict:
        response = self.session.get(f"{self.url}/wallet/did/public")
        response.raise_for_status()
        return response.json()["result"]

    def get_credential_definition(self, cred_def_id: str) -> dict:
        response = self.session.get(f"{self.url}/credential-definitions/{cred_def_id}")
        response.raise_for_status()
        return response.json()["credential_definition"]

    def get_schema(self, schema_id: str) -> dict:
        response = self.session.get(f"{self.url}/schemas/{schema_id}")
        response.raise_for_status()
        return response.json()["schema_json"]
