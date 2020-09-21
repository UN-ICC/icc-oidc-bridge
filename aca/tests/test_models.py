import pytest

from aca.models import PresentationFactory


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
