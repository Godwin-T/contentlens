# app/services/blog_service.py
from datetime import datetime
from api.db.database import SessionLocal
from api.v1.models.blog import BlogPost
from api.v1.schemas.blog import BlogPostCreate


def get_all_posts():
    """Fetch all blog posts"""
    db = SessionLocal()
    posts = db.query(BlogPost).order_by(BlogPost.created_at.desc()).all()
    db.close()
    return posts


def get_post_by_id(post_id: int):
    """Fetch a single blog post by ID"""
    db = SessionLocal()
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    db.close()
    return post


def create_blog_post(blog: BlogPostCreate):
    db = SessionLocal()
    new_post = BlogPost(
        title=blog.title, content=blog.content, created_at=datetime.utcnow()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    db.close()
    return new_post
