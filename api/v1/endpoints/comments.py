from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.services.comment_service import CommentService
from app.core.database.repositories.comment_repository import CommentRepository
from app.core.database.repositories.post_repository import PostRepository
from app.core.database.repositories.user_repository import UserRepository
from app.schemas.requests.comment import CommentCreateRequest
from app.schemas.responses.comment import CommentResponse
from app.core.config.dependencies import get_current_user, get_db
from app.models import User

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment_data: CommentCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a comment to a post"""
    service = CommentService(
        CommentRepository(db),
        PostRepository(db),
        UserRepository(db)
    )
    return await service.create_comment(comment_data, post_id, current_user.id)

@router.get("/", response_model=list[CommentResponse])
async def get_post_comments(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all comments for a post"""
    service = CommentService(
        CommentRepository(db),
        PostRepository(db),
        UserRepository(db)
    )
    return await service.get_post_comments(post_id)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    post_id: int,
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a comment"""
    service = CommentService(
        CommentRepository(db),
        PostRepository(db),
        UserRepository(db)
    )
    await service.delete_comment(comment_id, current_user.id)