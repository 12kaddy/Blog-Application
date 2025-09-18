from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config.dependencies import get_current_user
from app.core.database.models import User
from app.core.database.session import get_db
from app.core.exceptions.http_exceptions import UnauthorizedException
from app.core.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False
)

async def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
    db:Session = Depends(get_db)
) -> Optional[User]:
    """Dependency for optional authentication"""
    if not token:
        return None
    return await get_current_user(token, db)


async def get_current_user_required(
    token: str = Depends(oauth2_scheme),
        db:Session = Depends(get_db)
) -> User:
    """Dependency for required authentication"""
    if not token:
        raise UnauthorizedException("Not authenticated")
    return await get_current_user(token, db)