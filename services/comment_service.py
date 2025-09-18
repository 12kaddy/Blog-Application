from app.core.database.repositories.comment_repository import CommentRepository
from app.core.database.repositories.post_repository import PostRepository
from app.core.database.repositories.user_repository import UserRepository
from app.models import UserRole
from app.schemas.requests.comment import CommentCreateRequest
from app.schemas.responses.comment import CommentResponse
from app.core.exceptions.http_exceptions import (
    NotFoundException,
    ForbiddenException
)

class CommentService:
    def __init__(
            self,
            comment_repo: CommentRepository,
            post_repo: PostRepository,
            user_repo: UserRepository
    ):
        self.comment_repo = comment_repo
        self.post_repo = post_repo
        self.user_repo = user_repo

    async def create_comment(
            self,
            comment_data: CommentCreateRequest,
            post_id: int,
            user_id: int
            ) -> CommentResponse:
                """Add comment to post with validation"""
                if not await self.post_repo.get_by_id(post_id):
                    raise NotFoundException("Post not found")

                if not await self.user_repo.get_by_id(user_id):
                    raise NotFoundException("User not found")

                db_comment = await self.comment_repo.create_comment(
                    content=comment_data.content,
                    user_id=user_id,
                    post_id=post_id
                )
                return CommentResponse.model_validate(db_comment)

    async def get_post_comments(self, post_id: int) -> list[CommentResponse]:
            """Get all comments for a post"""
            if not await self.post_repo.get_by_id(post_id):
                raise NotFoundException("Post not found")

            comments = await self.comment_repo.get_by_post(post_id)
            return [CommentResponse.model_validate(comment) for comment in comments]

    async def delete_comment(self, comment_id: int, user_id: int) -> None:
        """Delete comment with ownership check"""
        comment = await self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundException("Comment not found")

        user = await self.user_repo.get_by_id(user_id)
        if comment.user_id != user_id and user.role != UserRole.ADMIN:
            raise ForbiddenException("You can only delete your own comments")

        await self.comment_repo.delete_comment(comment_id)