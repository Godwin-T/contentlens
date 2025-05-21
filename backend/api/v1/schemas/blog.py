# app/schemas/blog.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class BlogPostBase(BaseModel):
    title: str
    content: str
    description: str
    author: str
    published: str
    readTime: str
    slug: str
    category: str
    image: str


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostResponse(BlogPostBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True


class RetrievalRequest(BaseModel):
    article_id: str
    query: Optional[str] = None
    # k: int = 4
    # search_type: str = "similarity"
    # score_threshold: Optional[float] = None


class DocumentChunk(BaseModel):
    content: str
    metadata: dict


class RetrievalResponse(BaseModel):
    chunks: List[DocumentChunk]
    cache_hit: bool = False


class ChatRequest(BaseModel):
    user_id: str
    article_id: str
    query: str
