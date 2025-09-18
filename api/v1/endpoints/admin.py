from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories import UserRepository
from app.services.admin_service import AdminService
from app.schemas.responses.user import UserResponse
from app.core.config.dependencies import get_current_admin, get_db
from sqlalchemy.orm import Session
from app.models import User

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=list[UserResponse])
async def list_all_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """List all users (admin only)"""
    service = AdminService(UserRepository(db))
    return await service.list_users()

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Delete any user account (admin only)"""
    service = AdminService(UserRepository(db))
    await service.delete_user(user_id)