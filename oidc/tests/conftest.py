import pytest
from oidc.models import AuthSession, PresentationConfigurations
from django.utils import timezone
from datetime import timedelta
from oidc_provider.models import RSAKey


@pytest.fixture
def email_presentation_configuration():
    return PresentationConfigurations.objects.create(
        id="verified-email",
        subject_identifier="email",
        configuration={
            "name": "Basic Proof",
            "version": "1.0",
            "requested_attributes": [{"name": "email", "restrictions": []}],
            "requested_predicates": [],
        },
    )


@pytest.fixture
def name_presentation_configuration():
    return PresentationConfigurations.objects.create(
        id="verified-email",
        subject_identifier="name",
        configuration={
            "name": "Basic Proof",
            "version": "1.0",
            "requested_attributes": [{"name": "email", "restrictions": []}],
            "requested_predicates": [],
        },
    )


@pytest.fixture
def jwt_key():
    # kid 3e3ee3f767a83d16f3cee02eb5e5eb92
    return RSAKey.objects.create(
        key="""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAtkoI5r2r+7SNcqBUTRNiVoVGwtBzvWZQqaGvL44vjLvkTBmH
BkW1eLVMYH+V00b+lAoZ+Crynw3Nd7vGlP3tpTD2PIfOUFyrrL1ed8ghHbgeQflX
uoLg3/8X3lFNYsj2DkTgDzHaJI9ZswpRHNF+gVCfKGqvSYLOlPKeAfxnJybvf4WQ
1FDjDYuVY2h8t/ZM6IMbzqgAYJZW4unsS3D8n0JtwxNT//K6GjgcJdF5bJiI5Vvh
YjOTi45iMWvN9bWSPBCHR2YKjT7SbgihoCGVB0cq2ROOpEiU3IIZ6ZBY6IKVB5w8
frmsXBVyf8zmJeqHw+jF92xwCyljfNKkRTrW0QIDAQABAoIBAAjrU8bWflUb3yqT
UGH6Z3627rYW36g4xWGcw6b0B2eUxKA574gNs8oVijMpNaTXfcVd6SoMupUFu96h
QB+HfS/urAhc12ofNAHeZ4I84eyZAayrYpuBo+HR6Ce8mqi8Dy4LjgWwTsLTMMm4
i4IkI1MjJWZ43IggRQi3W6aFOcGJ6lP8IM0WFfNu1Cv3W7BanvmVmI2L+UnFvvA5
LkWSX0kkx/I2p6++UtdO7foInftcmRnak6TQWj73hqSFKhlk3APVOSf9lTlhCwre
1y6s71QuNApdLGwzRlIfOqH307iXv78BQf2W7kh04oLQPaOWXSWb8/oYBpE5EPq9
Xffn3PECgYEAy/xN8dNapDICQplnSAXJrOXYYZ6bHXTMQrQAHYxPVyCV+aG5sqVh
1sZj7tUAmWXAIPLAqmHbAaOM8tK4+WTdDvnYnWkuh2s0SM2mPqD++HllJq2Op+NQ
UbipAAPytrun47qSJOmrlw5/qPO27l4wRx5SangU4Q7sB7UT8lnsZf8CgYEA5MVx
W6I1Vnk5u/JHRi0KTAJNT5ktBPNRUEYb2bQdvvlK+DPFM2rnimwQNz6eocIWvu4p
TkFHFONJeed+45VLCpnvxXkx4VAp57sO4F/HHy31zCJ7GU/XzuWqvMS9pR9FiUVL
lSw9WtxJp7jJL1uvjKaQYFZBC77ZqB3iZ2md4y8CgYEAunvcnjoE4Zs+abhorXVt
HH28RfKECHfgzRJWEK1XU2Xc9iyd4e5D9d/FOHDObW6SKQ0Eij+Pwn3Mu6ldpdJK
LgjHuZCREwg08mHfm93/exUwHh4JDv9HTI6vIe56FAiWwiCsvsZJMn30w3abRGwj
YsEbw24oWGAV9C3dIHCJJ+0CgYEAx1gxDgsLdT2PDHHyn3jR1yfOXET6UK0BNvTQ
geSMYwPxytO5y7Mk7Z56htke+48XqOn4vkLtgIsJVJtfG0rVJ/i5URbpWw8yZMXA
Ec4DweyXmXiWUZkcUSIZpAG/yymzuwjR8ruo/wqjd+3yCT1YfDQL7JZcebKlEPRx
e3Ex7msCgYAWXjeXhOFkQNvmA8zTP+iC37iqOEsTc730P0cADbfumBsbGIE0oJuX
AvOCVR9tdci/jh2DbSxdB27hHw7BU2DU8ji71Ee97TQ1Fudkc4jpgFTyb2MZTy0Z
YHj3yqoO69+shd3fWFonlshgo1MIhArEn+IpP7aJJupMb3JG/RWEyQ==
-----END RSA PRIVATE KEY-----"""
    )


@pytest.fixture
def validated_session():
    return AuthSession.objects.create(
        id="0942a7b2-015d-420a-ac13-242694bcbf6f",
        presentation_record_id="verified-email",
        presentation_request_id="e2e1b664-5fd9-401d-96bc-26a62c4777a8",
        presentation_request={
            "@id": "e505dc2a-5320-478f-8c65-a68f04562a47",
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
            "comment": None,
            "~service": {
                "routingKeys": None,
                "recipientKeys": ["2BbGm6Mo9BVkXkn1YGjUoEUBB85Ba7XZW6qfgpMXD3XP"],
                "serviceEndpoint": "http://127.0.0.1:8090",
            },
            "request_presentations~attach": [
                {
                    "@id": "libindy-request-presentation-0",
                    "data": {
                        "base64": "eyJuYW1lIjogIkJhc2ljIFByb29mIiwgInZlcnNpb24iOiAiMS4wIiwgInJlcXVlc3RlZF9hdHRyaWJ1dGVzIjogeyJlMmQwMjJiMi0xNDNiLTRiNDctYjI4OS1lMmJhNzYyNTUyZjQiOiB7Im5hbWUiOiAiZW1haWwiLCAicmVzdHJpY3Rpb25zIjogW119fSwgInJlcXVlc3RlZF9wcmVkaWNhdGVzIjoge30sICJub25jZSI6ICIyMDUwOTE3MDc1Mzk4NDk3MDk3MTQyODg0MDIzNjQ5MDQyNDIxMTUifQ=="
                    },
                    "mime-type": "application/json",
                }
            ],
        },
        presentation_request_satisfied=True,
        expired_timestamp=timezone.now() + timedelta(days=1),
        request_parameters={
            "nonce": "vdoOCIrMvSRn2vYcgAV3vszUKb3ACJlD",
            "scope": "openid profile vc_authn",
            "state": "O8ALJmGFm5ByvYMyWhT7vkzdc3dc5Yds",
            "client_id": "770241",
            "redirect_uri": "http://127.0.0.1:8080/oidc/auth/cb/",
            "response_type": "code",
            "pres_req_conf_id": "verified-email",
        },
        presentation={
            "predicates": {},
            "revealed_attrs": {
                "e2d022b2-143b-4b47-b289-e2ba762552f4": {
                    "raw": "test@mail.org",
                    "encoded": "69775574976209370463886362368455342215648530278529236721860183817752792728556",
                    "sub_proof_index": 0,
                }
            },
            "unrevealed_attrs": {},
            "self_attested_attrs": {},
        },
    )
