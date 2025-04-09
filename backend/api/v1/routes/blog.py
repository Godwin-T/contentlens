# app/routes/blog.py
from fastapi import APIRouter, HTTPException, Depends
from api.dependency import verify_admin
from api.v1.services.blog_service import get_all_posts, get_post_by_id, create_blog_post
from api.v1.schemas.blog import BlogPostCreate, BlogPostResponse

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get("/")
def list_all_blog_posts():
    return get_all_posts()


@router.get("/{post_id}")
def get_blog_post(post_id: int):
    post = get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post(
    "/admin", response_model=BlogPostResponse, dependencies=[Depends(verify_admin)]
)
def create_blog(blog: BlogPostCreate):
    new_post = create_blog_post(blog)
    return new_post
