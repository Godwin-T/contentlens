# app/models/blog.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from api.db.database import Base


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False, server_default=func.now())
    description = Column(Text, nullable=False)
    author = Column(String(255), nullable=False)
    published = Column(String(100), nullable=False)
    readTime = Column(String(50), nullable=False)
    slug = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    image = Column(String(255), nullable=False)
