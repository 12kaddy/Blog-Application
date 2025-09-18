from datetime import date
from app.core.database.repositories.post_repository import PostRepository
from app.core.database.repositories.user_repository import UserRepository
from app.schemas.requests.post import PostCreateRequest, PostUpdateRequest
from app.schemas.responses.post import PostResponse
from app.core.exceptions.http_exceptions import NotFoundException, ForbiddenException

class PostService:
    def __init__(self, post_repository: PostRepository, user_repository: UserRepository):
        self.post_repo = post_repository
        self.user_repo = user_repository

    async def create_post(self, post_data: PostCreateRequest, user_id: int) -> PostResponse:
        """Create a new post with owner validation"""
        if not await self.user_repo.get_by_id(user_id):
            raise NotFoundException("User not found")

        post = await self.post_repo.create_post(
            title=post_data.title,
            content=post_data.content,
            user_id=user_id
        )
        return PostResponse.model_validate(post)

    async def update_post(self, post_id: int, post_data: PostUpdateRequest, user_id: int) -> PostResponse:
        """Update existing post with ownership check"""

        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise NotFoundException("Post not found")

        if post.user_id != user_id:
            raise ForbiddenException("You can only edit your own posts")

        updated_post = await self.post_repo.update_post(
            post_id=post_id,
            title=post_data.title,
            content=post_data.content
        )
        return PostResponse.model_validate(updated_post)

    async def get_all_posts(self) -> list[PostResponse]:
        """Get all posts"""

        posts = await self.post_repo.get_all()
        return [PostResponse.model_validate(post) for post in posts]

    async def get_posts_by_date_range(self, start_date: date, end_date: date) -> list[PostResponse]:
        """Get posts within a date range"""

        posts = await self.post_repo.get_by_date_range(start_date, end_date)
        return [PostResponse.model_validate(post) for post in posts]

    async def search_posts(self, keyword: str) -> list[PostResponse]:
        """Search posts by keyword"""

        posts = await self.post_repo.search(keyword)
        return [PostResponse.model_validate(post) for post in posts]

    async def get_post_by_id(self, post_id:int) -> PostResponse:
        """Get single post by id"""

        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise NotFoundException("Post not found")
        return PostResponse.model_validate(post)