import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings

class XAPIError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

async def _make_request(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {settings.X_BEARER_TOKEN}"
    }
    
    if not settings.X_BEARER_TOKEN:
        # Mock mode if token is missing (useful for basic testing without real API)
        raise XAPIError("X_BEARER_TOKEN is not configured", 500)

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            
            if response.status_code == 401:
                raise XAPIError("Unauthorized: Invalid X API Token", 401)
            elif response.status_code == 403:
                raise XAPIError("Forbidden: X API access denied", 403)
            elif response.status_code == 404:
                raise XAPIError("Resource not found on X", 404)
            elif response.status_code == 429:
                raise XAPIError("Rate limit exceeded on X API", 429)
            elif response.status_code >= 500:
                raise XAPIError(f"X API Server Error: {response.status_code}", response.status_code)
                
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                # Catch 402 or other unhandled 4xx/5xx errors
                raise XAPIError(f"X API Error: {e.response.status_code} {e.response.reason_phrase}", e.response.status_code)
                
            data = response.json()
            if "errors" in data and len(data["errors"]) > 0:
                 raise XAPIError(f"X API Error: {data['errors'][0].get('detail', 'Unknown error')}", 400)
            return data
            
        except httpx.RequestError as e:
            raise XAPIError(f"Network error communicating with X API: {str(e)}", 503)

async def get_user_by_username(username: str) -> Dict[str, Any]:
    # Use official X API v2 endpoint
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    params = {
        "user.fields": "created_at,description,public_metrics,profile_image_url,verified"
    }
    data = await _make_request(url, params)
    
    if "data" not in data:
        raise XAPIError(f"User {username} not found", 404)
        
    raw_user = data["data"]
    metrics = raw_user.get("public_metrics", {})
    
    # Normalize user data
    return {
        "id": raw_user.get("id"),
        "username": raw_user.get("username"),
        "name": raw_user.get("name"),
        "description": raw_user.get("description", ""),
        "created_at": raw_user.get("created_at"),
        "profile_image_url": raw_user.get("profile_image_url", ""),
        "followers_count": metrics.get("followers_count", 0),
        "following_count": metrics.get("following_count", 0),
        "post_count": metrics.get("tweet_count", 0),
        "verified": raw_user.get("verified", False)
    }

async def get_user_posts(user_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,public_metrics,referenced_tweets,entities",
        "exclude": "retweets,replies" # Can be adjusted based on needs, but let's fetch all initially if we want to analyze reply ratios
    }
    # For accurate reply/repost ratios, we should NOT exclude them.
    params.pop("exclude") 

    try:
        data = await _make_request(url, params)
    except XAPIError as e:
        if e.status_code == 404:
            return [] # No posts found
        raise
        
    raw_posts = data.get("data", [])
    normalized_posts = []
    
    for p in raw_posts:
        metrics = p.get("public_metrics", {})
        refs = p.get("referenced_tweets", [])
        
        is_reply = any(r.get("type") == "replied_to" for r in refs)
        is_repost = any(r.get("type") == "retweeted" for r in refs)
        is_quote = any(r.get("type") == "quoted" for r in refs)
        
        entities = p.get("entities", {})
        hashtags = [h.get("tag") for h in entities.get("hashtags", [])]
        mentions = [m.get("username") for m in entities.get("mentions", [])]
        urls = [u.get("expanded_url") for u in entities.get("urls", [])]
        
        normalized_posts.append({
            "id": p.get("id"),
            "text": p.get("text", ""),
            "created_at": p.get("created_at"),
            "like_count": metrics.get("like_count", 0),
            "reply_count": metrics.get("reply_count", 0),
            "repost_count": metrics.get("retweet_count", 0),
            "quote_count": metrics.get("quote_count", 0),
            "is_reply": is_reply,
            "is_repost": is_repost,
            "is_quote": is_quote,
            "hashtags": hashtags,
            "mentions": mentions,
            "urls": urls
        })
        
    return normalized_posts
