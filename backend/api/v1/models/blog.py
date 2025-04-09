# app/models/blog.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from api.db.database import Base


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
