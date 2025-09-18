from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.models.comment import Comment

class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, comment_id: int) -> Comment | None:
        result = await self.db.execute(select(Comment).filter(Comment.id == comment_id))
        return result.scalars().first()

    async def create_comment(self, content: str, user_id: int, post_id: int) -> Comment:
        db_comment = Comment(
            content=content,
            user_id=user_id,
            post_id=post_id
        )
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)
        return db_comment

    async def get_by_post(self, post_id: int) -> list[Comment]:
        result = await self.db.execute(select(Comment).filter(Comment.post_id == post_id))
        return result.scalars().all()

    async def get_by_user(self, user_id: int) -> list[Comment]:
        result = await self.db.execute(select(Comment).filter(Comment.user_id == user_id))
        return result.scalars().all()

    async def delete_comment(self, comment_id: int) -> bool:
        comment = await self.get_by_id(comment_id)
        if not comment:
            return False

        await self.db.delete(comment)
        await self.db.commit()
        return True