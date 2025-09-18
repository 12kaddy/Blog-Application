from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories import UserRepository
from app.services.user_service import UserService
from app.schemas.requests.user import UserCreateRequest
from app.schemas.responses.user import UserResponse
from app.core.config.dependencies import get_current_user, get_db
from app.models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
        user_data: UserCreateRequest,
        db: AsyncSession = Depends(get_db)
):
    service = UserService(UserRepository(db))
    return await service.register_user(user_data)

@router.get("/user", response_model=UserResponse)
async def get_current_user_profile(
    user: User = Depends(get_current_user)
):
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(UserRepository(db))
    await service.delete_user(user_id, user.role)
