# app/schemas/blog.py
from pydantic import BaseModel
from datetime import datetime


class BlogPostBase(BaseModel):
    title: str
    content: str


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostResponse(BlogPostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
