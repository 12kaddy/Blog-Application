from datetime import date
from sqlalchemy import select, or_, func, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.models.post import Post

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_post(self, title: str, content: str, user_id: int) -> Post:
        db_post = Post(title=title, content=content, user_id=user_id)
        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)
        return db_post

    async def get_by_id(self, post_id: int) -> Post | None:
        result = await self.db.execute(select(Post).filter(Post.id == post_id))
        return result.scalars().first()

    async def get_all(self) -> Sequence[Post]:
        result = await self.db.execute(select(Post))
        return result.scalars().all()

    async def get_by_user(self, user_id: int) -> Sequence[Post]:
        result = await self.db.execute(select(Post).filter(Post.user_id == user_id))
        return result.scalars().all()

    async def update_post(self, post_id: int, **kwargs) -> Post | None:
        post = await self.get_by_id(post_id)
        if not post:
            return None

        for key, value in kwargs.items():
            setattr(post, key, value)

        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def search(self, keyword: str) -> Sequence[Post]:
        result = await self.db.execute(
            select(Post).filter(
                or_(
                    Post.title.ilike(f"%{keyword}%"),
                    Post.content.ilike(f"%{keyword}%")
                )
            )
        )
        return result.scalars().all()

    async def get_by_date_range(self, start: date, end: date) -> Sequence[Post]:
        result = await self.db.execute(
            select(Post).filter(
                Post.created_at.between(start, end)
            )
        )
        return result.scalars().all()