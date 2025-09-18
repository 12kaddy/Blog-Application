from pydantic import BaseModel

class TokenResponse(BaseModel):
    """Standard token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None
    refresh_token: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOi...",
                "token_type": "bearer",
                "expires_in": 3600,
                "refresh_token": "eyJhbGciOi...",
            }
        }