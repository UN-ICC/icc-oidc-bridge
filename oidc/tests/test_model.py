import pytest
import json
from django.utils import timezone


@pytest.mark.django_db
class TestPresentationConfigurationModel:
    def test_to_json(self, revocation_presentation_configuration):
        assert revocation_presentation_configuration.to_json() == {
            "proof_request": {
                "name": "Basic Proof",
                "version": "1.0",
                "requested_attributes": {
                    "email1": {
                        "label": "email1",
                        "name": "email",
                        "non_revoked": {"to": 1656914015, "from": 1656914015},
                        "restrictions": [],
                    }
                },
                "requested_predicates": {},
                "non_revoked": {"to": 1656914015, "from": 1656914015},
            }
        }

    def test_to_json_no_to(self, revocation_no_to_presentation_configuration):
        presentation = revocation_no_to_presentation_configuration.to_json()
        assert "to" in presentation['proof_request']['non_revoked']
        now = int(timezone.now().timestamp())
        assert ((now - 300) <= presentation['proof_request']['non_revoked']["to"] <= (now + 300))

    def test_to_json_no_revocation(self, revocation_no_revocation_presentation_configuration):
        assert revocation_no_revocation_presentation_configuration.to_json() == {
            "proof_request": {
                "name": "Basic Proof",
                "version": "1.0",
                "requested_attributes": {
                    "email1": {
                        "label": "email1",
                        "name": "email",
                        "restrictions": [],
                    }
                },
                "requested_predicates": {},
            }
        }
