# app/routes/blog.py
from fastapi import APIRouter, HTTPException, Depends
from api.dependency import verify_admin
from api.v1.services.blog_service import get_all_posts, get_post_by_id, create_blog_post
from api.v1.services.ai_service import (
    read_item,
    retrieve_documents,
    invalidate_retrieval_cache,
    get_retrieval_stats,
    chat,
    reset_conversation,
)
from api.v1.schemas.blog import BlogPostCreate, BlogPostResponse, RetrievalRequest

router = APIRouter(prefix="/api/v1", tags=["Blog"])


@router.get("/")
def list_all_blog_posts():
    return get_all_posts()


@router.get("/health")
def health():
    return {"status", "ok"}


@router.get("/search/{post_id}")
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


@router.get("/ai-search")
def search_item(q: str, neural: bool = True):
    return read_item(q, neural)


# @router.post("/retrieve")
# def retrieve_blog_documents(request: RetrievalRequest):
#     try:
#         return retrieve_documents(request)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/invalidate-cache/{article_id}")
def invalidate_cache(article_id: str):
    return invalidate_retrieval_cache(article_id)


@router.get("/retrieval-stats")
def get_stats():
    return get_retrieval_stats()


@router.post("/ask")
def rag_chat(user_id: str, article_id: str, query: str):
    return chat(user_id, article_id, query)


@router.get("/reset-conn")
def reset(user_id: str, article_id: str):
    return reset_conversation(user_id, article_id)
