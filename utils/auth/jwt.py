from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config.settings import settings
from typing import Dict, Any

def create_access_token(
    data: Dict[str, Any],
    expires_delta: timedelta | None = None
) -> str:
    """
    Creates a signed JWT with:
    - Standard claims (exp, iat)
    - Custom payload data
    - HS256 signing by default
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "iss": settings.JWT_ISSUER
    })
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def verify_token(token: str) -> Dict[str, Any]:
    """
    Validates JWT and returns payload if valid.
    Raises JWTError for:
    - Expired tokens
    - Invalid signatures
    - Missing claims
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={
                "require_exp": True,
                "require_iat": True,
                "verify_iss": True,
                "verify_signature": True
            },
            issuer=settings.JWT_ISSUER
        )
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")

def decode_token_unverified(token: str) -> Dict[str, Any]:
    """
    For safely reading expired tokens (e.g., during refresh)
    Only use for non-security purposes like analytics
    """
    return jwt.get_unverified_claims(token)