from app.core.database.repositories.user_repository import UserRepository
from app.schemas.requests.user import UserCreateRequest
from app.schemas.responses.user import UserResponse
from app.core.exceptions.http_exceptions import (
    NotFoundException,
    ConflictException,
    ForbiddenException
)
from app.models.role import UserRole
from app.utils import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    async def register_user(self, user_data: UserCreateRequest) -> UserResponse:
        """Register a new user with validation"""
        if await self.user_repo.get_by_email(user_data.email):
            raise ConflictException("Email already registered")

        if await self.user_repo.get_by_username(user_data.username):
            raise ConflictException("Username already taken")

        if user_data.role == UserRole.ADMIN:
            raise ForbiddenException("Admin registration requires special privileges")

        hashed = hash_password(user_data.password)
        user = await self.user_repo.create_user(
            username = user_data.username,
            email=user_data.email,
            hash_password = hashed,
            role=user_data.role
        )
        return UserResponse.model_validate(user)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """Get user details by ID"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: int, requester_role: UserRole) -> None:
        """Delete user with permission checks"""
        if requester_role != UserRole.ADMIN:
            raise ForbiddenException("Only admins can delete users")

        if not await self.user_repo.delete_user(user_id):
            raise NotFoundException("User not found")