from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.models.user import User
from app.schemas.requests.user import UserCreateRequest
from app.utils.hashing import hash_password


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def get_all(self) -> Sequence[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def create_user(self, user_data: UserCreateRequest) -> User:
        db_user = User(
            username=user_data.username,
            email=str(user_data.email),  # Convert EmailStr
            hashed_password=hash_password(user_data.password),
            role=user_data.role
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()
        return True