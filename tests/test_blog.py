# backend/tests/test_blog_service.py

from unittest.mock import MagicMock, patch

from api.v1.models.blog import BlogPost
from api.v1.schemas.blog import BlogPostCreate
from api.v1.services.blog_service import get_post_by_id, get_all_posts, create_blog_post


def test_get_post_by_id_returns_post():
    mock_post = BlogPost(id=1, title="Mock Title", content="Mock Content")

    with patch("api.v1.services.blog_service.SessionLocal") as mock_session_local:
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_filter.first.return_value = mock_post
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        mock_session_local.return_value = mock_db

        result = get_post_by_id(1)
        assert result == mock_post
        assert result.title == "Mock Title"


def test_get_all_posts_returns_list():
    mock_posts = [
        BlogPost(id=1, title="Post 1", content="Content 1"),
        BlogPost(id=2, title="Post 2", content="Content 2"),
    ]

    with patch("api.v1.services.blog_service.SessionLocal") as mock_session_local:
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_order_by = MagicMock()

        # Chain the mock: query().order_by().all() => mock_posts
        mock_order_by.all.return_value = mock_posts
        mock_query.order_by.return_value = mock_order_by
        mock_db.query.return_value = mock_query
        mock_session_local.return_value = mock_db

        result = get_all_posts()

        assert len(result) == 2
        assert result[0].title == "Post 1"


def test_create_blog_post():
    blog_data = BlogPostCreate(title="New Blog", content="New Content",
                               description="A short summary of the post.",
                               author="John Doe", published="true", readTime="5 min",
                               slug="my-first-blog-post", category="Technology",
                               image="https://example.com/image.jpg") 
    
    mock_new_post = BlogPost(
        id=1,
        title=blog_data.title,
        content=blog_data.content,
        description=blog_data.description,
        author=blog_data.author,
        published=blog_data.published,
        readTime=blog_data.readTime,
        slug=blog_data.slug,
        category=blog_data.category,
        image=blog_data.image

    )

    with patch("api.v1.services.blog_service.SessionLocal") as mock_session_local:

            mock_db = MagicMock()
            mock_session_local.return_value = mock_db

            # mimic .refresh() populating the new_post object
            def refresh_side_effect(post_obj):
                post_obj.id = mock_new_post.id

            mock_db.refresh.side_effect = refresh_side_effect

            result = create_blog_post(blog_data)

            assert result.title == "New Blog"
            assert result.content == "New Content"
