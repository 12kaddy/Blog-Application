from typing import Annotated

from pydantic import BaseModel, Field


class UserLoginRequest(BaseModel):
    username: Annotated[
        str,
        Field(min_length=3, max_length=50, json_schema_extra={"example": "john_doe"})
    ]
    password: Annotated[
        str,
        Field(min_length=8, max_length=64, json_schema_extra={"example": "SecurePass123!"})
    ]

class RefreshTokenRequest(BaseModel):
    """Token refresh schema"""
    refresh_token: Annotated[str, Field(...)]