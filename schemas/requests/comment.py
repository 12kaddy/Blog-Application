from pydantic import BaseModel, Field

class CommentCreateRequest(BaseModel):
    """Comment creation schema"""
    content: str = Field(..., min_length=1, max_length=500)

class CommentUpdateRequest(BaseModel):
    """Comment update schema"""
    content: str = Field(..., min_length=1, max_length=500)