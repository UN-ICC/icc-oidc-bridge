from marshmallow import fields, post_load, ValidationError, Schema

from aca.utils import encode_base64, decode_base64


class PresentationData(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return {"base64": encode_base64(value)}

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return decode_base64(value.get("base64", ""))
        except ValueError as error:
            raise ValidationError("Should be a base64 string") from error


class PresentationAttach:
    def __init__(
        self,
        data: dict,
        id: str = "libindy-request-presentation-0",
        mime_type: str = "application/json",
    ):
        self.data = data
        self.mime_type = mime_type
        self.id = id


class Service:
    def __init__(
        self, recipient_keys: str, service_endpoint: str, routing_keys: str = None
    ):
        self.recipient_keys = recipient_keys
        self.routing_keys = routing_keys
        self.service_endpoint = service_endpoint


class Presentation:
    def __init__(
        self,
        presentation: [PresentationAttach],
        service: Service,
        id: str,
        type: str = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
        comment: str = None,
    ):
        self.presentation = presentation
        self.service = service
        self.id = id
        self.type = type
        self.comment = comment


class ServiceSchema(Schema):
    recipient_keys = fields.List(fields.Str(), data_key="recipientKeys")
    routing_keys = fields.List(fields.Str(), data_key="routingKeys", allow_none=True)
    service_endpoint = fields.Str(data_key="serviceEndpoint")

    @post_load
    def make_service(self, data, **kwargs):
        return Service(**data)


class PresentationAttachSchema(Schema):
    id = fields.Str(data_key="@id")
    mime_type = fields.Str(data_key="mime-type")
    data = PresentationData(data_key="data")

    @post_load
    def make_presentation_attach(self, data, **kwargs):
        return PresentationAttach(**data)


class PresentationSchema(Schema):
    type = fields.Str(data_key="@type")
    id = fields.Str(data_key="@id")
    service = fields.Nested(ServiceSchema, data_key="~service")
    presentation = fields.Nested(
        PresentationAttachSchema, data_key="request_presentations~attach", many=True
    )
    comment = fields.Str(allow_none=True)

    @post_load
    def make_presentation(self, data, **kwargs):
        return Presentation(**data)


class PresentationFactory:
    presentation_schema = PresentationSchema()

    def __init__(self, presentation: Presentation):
        self.presentation = presentation

    @classmethod
    def from_params(
        cls, presentation_request: dict, p_id: str, verkey: [str], endpoint: str
    ):
        presentation = Presentation(
            presentation=[PresentationAttach(data=presentation_request)],
            service=Service(recipient_keys=verkey, service_endpoint=endpoint),
            id=p_id,
        )
        return cls(presentation)

    @classmethod
    def from_json(cls, presentation_request: dict):
        presentation = PresentationFactory.presentation_schema.load(
            presentation_request
        )
        return cls(presentation)

    def to_json(self):
        return self.presentation_schema.dump(self.presentation)
