from app.core.database.repositories.user_repository import UserRepository
from app.schemas.responses.user import UserResponse
from app.core.exceptions.http_exceptions import NotFoundException, ForbiddenException
from app.models.role import UserRole
from sqlalchemy.orm import Session


class AdminService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    async def list_users(self) -> list[UserResponse]:
        users = await self.user_repo.get_all()
        return [UserResponse.model_validate(user) for user in users]

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise NotFoundException("User not found")

        if user.role == UserRole.ADMIN:
            raise ForbiddenException("Cannot delete other admin users")

        await self.user_repo.delete_user(user_id)