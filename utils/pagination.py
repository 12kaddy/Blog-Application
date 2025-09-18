from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.sql import Select
from math import ceil

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard pagination response format"""
    items: List[T] = Field(default_factory=list)
    total: int = Field(..., ge=0, examples=[100])
    page: int = Field(1, ge=1, examples=[1])
    per_page: int = Field(10, ge=1, le=100, examples=[10])
    total_pages: int = Field(..., ge=0, examples=[10])

    @classmethod
    def from_query(
            cls,
            query: Select,
            page: int,
            per_page: int,
            db_executor: callable
    ) -> 'PaginatedResponse':
        """SQLAlchemy-aware pagination builder"""
        # Count total items (optimized)
        total = db_executor(query.with_only_columns([func.count()])).scalar()

        # Apply pagination
        items = db_executor(
            query.offset((page - 1) * per_page)
            .limit(per_page)
        ).all()

        return cls(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=ceil(total / per_page) if total else 0
        )


async def async_paginate(
    query: Select,
    db_session,  # Required parameter first
    page: int = 1,
    per_page: int = 10
) -> PaginatedResponse:
    """Corrected async pagination with proper parameter order"""
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10
    # Async count
    total = (await db_session.execute(
        query.with_only_columns([func.count()])
    )).scalar()
    # Async results
    items = (await db_session.execute(
        query.offset((page - 1) * per_page)
        .limit(per_page)
    )).scalars().all()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=ceil(total / per_page) if total else 0
    )