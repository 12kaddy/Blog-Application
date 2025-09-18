from pydantic import BaseModel, Field
from typing import Annotated


class PostCreateRequest(BaseModel):
    """Post creation schema"""
    title: Annotated[str, Field(..., min_length=5, max_length=100)]
    content: Annotated[str, Field(..., min_length=10)]

class PostUpdateRequest(BaseModel):
    """Post update schema"""
    title: str | None = Field(None, min_length=5, max_length=100)
    content: str | None = Field(None, min_length=10)