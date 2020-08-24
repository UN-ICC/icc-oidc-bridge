import jwt
from oidc_provider.models import RSAKey
from django.utils import timezone
from datetime import timedelta


def build_jwt(
    claims: dict,
    not_before: int,
    not_after: int,
    audience: str,
    issuer: str,
    key: RSAKey,
    algorithm: str = "RS256",
) -> str:
    mandatory_claims = {
        "aud": audience,
        "iss": issuer,
        "iat": timezone.now(),
        "nbf": not_before,
        "exp": not_after,
    }

    claims.update(mandatory_claims)
    encoded_jwt = jwt.encode(claims, key, algorithm=algorithm)

    return encoded_jwt.decode("utf-8")


def token(lifetime, issuer, audiences, claims, kid: str):
    not_before = timezone.now()
    not_after = timezone.now() + timedelta(minutes=lifetime)

    key = [x for x in RSAKey.objects.all() if x.kid == kid]
    if not key:
        raise Exception(f"Key with kid {kid} not found")

    jwt_token = build_jwt(
        claims=claims,
        not_before=not_before,
        not_after=not_after,
        audience=audiences,
        issuer=issuer,
        key=key[0].key,
    )

    return jwt_token
