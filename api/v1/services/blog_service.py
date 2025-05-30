# app/services/blog_service.py
from api.db.database import SessionLocal
from api.v1.models.blog import BlogPost
from api.v1.schemas.blog_schema import BlogPostCreate
from api.ai_core.init_blogposts_collection import upload_single_embeddings


def get_all_posts():
    """Fetch all blog posts"""
    db = SessionLocal()
    posts = db.query(BlogPost).order_by(BlogPost.date.desc()).all()
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
        title=blog.title,
        content=blog.content,
        description=blog.description,
        author=blog.author,
        published=blog.published,
        readTime=blog.readTime,
        slug=blog.slug,
        category=blog.category,
        image=blog.image,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    db.close()
    data = {"content": new_post.content, "id": new_post.id, "title": new_post.title}
    upload_single_embeddings(data)
    return new_post
