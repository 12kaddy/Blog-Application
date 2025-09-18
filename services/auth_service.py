from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.core.database.repositories.user_repository import UserRepository
from app.schemas.responses.auth import TokenResponse
from app.utils.auth.jwt import create_access_token
from app.utils.hashing import verify_password
from app.core.exceptions.http_exceptions import UnauthorizedException


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def authenticate_user(self, username: str, password: str) -> TokenResponse:
        user = await self.user_repo.get_by_username(username)

        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid username or password")

        token_data = {
            'sub': str(user.id),
            'role': user.role.value
        }

        return TokenResponse(
            access_token=create_access_token(token_data),
            token_type="bearer"
        )