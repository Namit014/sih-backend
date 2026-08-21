import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_x_user():
    return {
        "data": {
            "id": "12345",
            "username": "testuser",
            "name": "Test User",
            "description": "Just a test user",
            "created_at": "2020-01-01T12:00:00.000Z",
            "profile_image_url": "http://example.com/image.jpg",
            "verified": False,
            "public_metrics": {
                "followers_count": 1000,
                "following_count": 500,
                "tweet_count": 2000
            }
        }
    }

@pytest.fixture
def mock_x_posts():
    return {
        "data": [
            {
                "id": "1",
                "text": "Hello world #test",
                "created_at": "2023-01-01T12:00:00.000Z",
                "public_metrics": {
                    "like_count": 10,
                    "reply_count": 2,
                    "retweet_count": 5,
                    "quote_count": 0
                },
                "entities": {
                    "hashtags": [{"tag": "test"}],
                    "mentions": [],
                    "urls": []
                },
                "referenced_tweets": []
            },
            {
                "id": "2",
                "text": "Reply to someone",
                "created_at": "2023-01-02T12:00:00.000Z",
                "public_metrics": {
                    "like_count": 2,
                    "reply_count": 1,
                    "retweet_count": 0,
                    "quote_count": 0
                },
                "entities": {},
                "referenced_tweets": [{"type": "replied_to"}]
            }
        ]
    }

@pytest.fixture
def mock_httpx_client(mock_x_user, mock_x_posts):
    # This is a simple fixture, but in the actual test we'll use `respx` or `patch` 
    # to mock `_make_request` directly for simplicity.
    pass
