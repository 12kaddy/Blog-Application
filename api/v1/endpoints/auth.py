from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.core.config.dependencies import get_db
from app.core.exceptions.http_exceptions import UnauthorizedException
from app.services.auth_service import AuthService  # Added import
from app.schemas.responses.auth import TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    try:
        service = AuthService(db)
        return await service.authenticate_user(form_data.username, form_data.password)
    except Exception as e:
        raise UnauthorizedException(detail=str(e))