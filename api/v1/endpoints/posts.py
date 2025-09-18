from fastapi import APIRouter, Depends, Query, status
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.services.post_service import PostService
from app.core.database.repositories.post_repository import PostRepository
from app.core.database.repositories.user_repository import UserRepository
from app.schemas.requests.post import PostCreateRequest, PostUpdateRequest
from app.schemas.responses.post import PostResponse
from app.core.config.dependencies import get_current_user, get_db
from app.models import User

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Create a new post"""
    service = PostService(PostRepository(db), UserRepository(db))
    return service.create_post(post_data, user.id)

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a single post by ID"""
    service = PostService(PostRepository(db), UserRepository(db))
    return service.get_post_by_id(post_id)

@router.get("/", response_model=list[PostResponse])
async def list_posts(
    keyword: str | None = Query(None, min_length=2),
    start_date: date | None = None,
    end_date: date | None = None,
    db: AsyncSession = Depends(get_db)
):
    """List posts with optional filters"""
    service = PostService(PostRepository(db), UserRepository(db))
    if keyword:
        return service.search_posts(keyword)
    elif start_date and end_date:
        return service.get_posts_by_date_range(start_date, end_date)
    return service.get_all_posts()

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a post"""
    service = PostService(PostRepository(db), UserRepository(db))
    return await service.update_post(post_id, post_data, current_user.id)