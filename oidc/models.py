from django.db import models
import uuid
from model_utils.models import TimeStampedModel
from django.conf import settings


def disambiguate_referent(referent: str) -> str:
    ref_idx = 1
    ref_split = referent.split("~")
    if len(ref_split) > 1:
        old_idx = int(ref_split[-1])
        ref_idx += old_idx

    return f"{ref_split[0]}~{ref_idx}"


# Create your models here.


class PresentationConfigurations(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    subject_identifier = models.CharField(max_length=255)
    configuration = models.JSONField()

    def __str__(self):
        return f"{self.id}"

    def to_json(self):
        presentation_request = {
            "name": self.configuration.get("name", ""),
            "version": self.configuration.get("version", ""),
            "requested_attributes": {},
            "requested_predicates": {},
        }

        for attr in self.configuration.get("requested_attributes", []):
            label = attr.get("label", str(uuid.uuid4()))
            if label in presentation_request.get("requested_attributes", {}).keys():
                label = disambiguate_referent(label)
            presentation_request["requested_attributes"].update({label: attr})

        for attr in self.configuration.get("requested_predicates", []):
            label = attr.get("label", str(uuid.uuid4()))
            if label in presentation_request.get("requested_predicates", {}).keys():
                label = disambiguate_referent(label)

            presentation_request["requested_predicates"].update({label: attr})

        return {"proof_request": presentation_request}


class AuthSession(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presentation_record_id = models.CharField(max_length=255)
    presentation_request_id = models.CharField(max_length=255)
    presentation_request = models.JSONField()
    presentation_request_satisfied = models.BooleanField(default=False)
    expired_timestamp = models.DateTimeField(blank=True, null=True)
    request_parameters = models.JSONField()
    presentation = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.presentation_record_id} - {self.presentation_request_id}"

    def satisfy_session(self, presentation):
        self.presentation_request_satisfied = True
        self.presentation = presentation
        self.save()


class MappedUrl(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.TextField()
    session = models.ForeignKey(
        AuthSession, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.id}"

    def get_short_url(self):
        return f"{settings.SITE_URL}/url/{self.id}"
