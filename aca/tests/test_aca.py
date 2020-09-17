import pytest
from aca.aca import PresentationFactory, ACAClient


@pytest.mark.django_db
class TestPresentation:
    def test_create_presentation_from_params(self):
        presentation = PresentationFactory.from_params(
            presentation_request={
                "name": "Basic Proof",
                "version": "1.0",
                "requested_attributes": {
                    "7948a556-3137-4e38-9ec2-11954b97652a": {
                        "name": "email",
                        "restrictions": [],
                    }
                },
                "requested_predicates": {},
                "nonce": "523327307422556114630448",
            },
            p_id="id",
            verkey=["verkey"],
            endpoint="endpoint",
        )
        assert presentation.to_json() == {
            "request_presentations~attach": [
                {
                    "@id": "libindy-request-presentation-0",
                    "data": {
                        "base64": "eyJuYW1lIjogIkJhc2ljIFByb29mIiwgInZlcnNpb24iOiAiMS4wIiwgInJlcXVlc3RlZF9hdHRyaWJ1dGVzIjogeyI3OTQ4YTU1Ni0zMTM3LTRlMzgtOWVjMi0xMTk1NGI5NzY1MmEiOiB7Im5hbWUiOiAiZW1haWwiLCAicmVzdHJpY3Rpb25zIjogW119fSwgInJlcXVlc3RlZF9wcmVkaWNhdGVzIjoge30sICJub25jZSI6ICI1MjMzMjczMDc0MjI1NTYxMTQ2MzA0NDgifQ=="
                    },
                    "mime-type": "application/json",
                }
            ],
            "~service": {
                "serviceEndpoint": "endpoint",
                "recipientKeys": ["verkey"],
                "routingKeys": None,
            },
            "comment": None,
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
            "@id": "id",
        }

    def test_create_presentation_from_json(self):
        presentation_json = {
            "request_presentations~attach": [
                {
                    "@id": "libindy-request-presentation-0",
                    "data": {
                        "base64": "eyJuYW1lIjogIkJhc2ljIFByb29mIiwgInZlcnNpb24iOiAiMS4wIiwgInJlcXVlc3RlZF9hdHRyaWJ1dGVzIjogeyI3OTQ4YTU1Ni0zMTM3LTRlMzgtOWVjMi0xMTk1NGI5NzY1MmEiOiB7Im5hbWUiOiAiZW1haWwiLCAicmVzdHJpY3Rpb25zIjogW119fSwgInJlcXVlc3RlZF9wcmVkaWNhdGVzIjoge30sICJub25jZSI6ICI1MjMzMjczMDc0MjI1NTYxMTQ2MzA0NDgifQ=="
                    },
                    "mime-type": "application/json",
                }
            ],
            "~service": {
                "serviceEndpoint": "endpoint",
                "recipientKeys": ["verkey"],
                "routingKeys": None,
            },
            "comment": None,
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
            "@id": "id",
        }

        presentation = PresentationFactory.from_json(presentation_json)
        assert presentation.to_json() == presentation_json


class TestAcaClient:
    def test_create_proof_request(self, requests_mock):
        url = "http://127.0.0.1"
        client = ACAClient(url, url, "token")
        mock_result = {"result": 0}
        requests_mock.post(f"{url}/present-proof/create-request", json=mock_result)
        result = client.create_proof_request({})
        assert result == mock_result

    def test_get_public_did(self, requests_mock):
        url = "http://127.0.0.1"
        client = ACAClient(url, url, "token")
        mock_result = {"result": 0}
        requests_mock.get(f"{url}/wallet/did/public", json=mock_result)
        result = client.get_public_did()
        assert result == 0

    def test_get_endpoint_url(self):
        url = "http://127.0.0.1"
        client = ACAClient(url, url, "token")
        result = client.get_endpoint_url()
        assert result == url
