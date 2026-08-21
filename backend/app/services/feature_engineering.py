import json
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
import numpy as np

# Load feature schema at startup to ensure we always output the exact list
with open("../ml/models/feature_schema.json", "r") as f:
    SCHEMA = json.load(f)
    EXPECTED_FEATURES = SCHEMA.get("features", [])

def _calculate_account_age_days(created_at: str) -> int:
    if not created_at:
        return 0
    try:
        # Example format: "2010-12-08T15:06:51.000Z"
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        return max((now - dt).days, 0)
    except Exception:
        return 0

def extract_features(user_data: Dict[str, Any], posts_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Initialize all expected features with 0
    features = {f: 0.0 for f in EXPECTED_FEATURES}
    
    # 1. Profile features
    features['account_age_days'] = float(_calculate_account_age_days(user_data.get("created_at")))
    features['followers_count'] = float(user_data.get("followers_count", 0))
    features['following_count'] = float(user_data.get("following_count", 0))
    features['post_count'] = float(user_data.get("post_count", 0))
    
    following = max(features['following_count'], 1.0)
    features['followers_following_ratio'] = features['followers_count'] / following
    
    # Profile completeness: has description and profile image
    completeness = 0.5
    if user_data.get("description"): completeness += 0.25
    if user_data.get("profile_image_url") and "default_profile_images" not in user_data.get("profile_image_url"):
        completeness += 0.25
    features['profile_completeness'] = completeness
    features['verified'] = 1.0 if user_data.get("verified") else 0.0
    
    # 2. Activity, Engagement, Content features from posts
    n_posts = len(posts_data)
    if n_posts > 0:
        # Time-based metrics
        try:
            dates = [datetime.fromisoformat(p["created_at"].replace("Z", "+00:00")) for p in posts_data if p.get("created_at")]
            dates.sort()
            if len(dates) > 1:
                timespan_days = max((dates[-1] - dates[0]).total_seconds() / 86400, 1.0)
                features['posts_per_day'] = len(dates) / timespan_days
                
                intervals = [(dates[i] - dates[i-1]).total_seconds() / 3600 for i in range(1, len(dates))] # hours
                features['average_post_interval'] = float(np.mean(intervals))
                features['posting_interval_std'] = float(np.std(intervals))
                features['activity_burst_score'] = features['posting_interval_std'] / max(features['average_post_interval'], 1.0)
            else:
                features['posts_per_day'] = 1.0
        except Exception:
            pass

        # Ratios
        replies = sum(1 for p in posts_data if p.get("is_reply"))
        reposts = sum(1 for p in posts_data if p.get("is_repost"))
        features['reply_ratio'] = replies / n_posts
        features['repost_ratio'] = reposts / n_posts
        features['original_post_ratio'] = max(0.0, 1.0 - features['reply_ratio'] - features['repost_ratio'])
        
        # Engagement
        likes = [p.get("like_count", 0) for p in posts_data]
        features['average_likes'] = float(np.mean(likes))
        features['average_replies'] = float(np.mean([p.get("reply_count", 0) for p in posts_data]))
        features['average_reposts'] = float(np.mean([p.get("repost_count", 0) for p in posts_data]))
        features['average_quotes'] = float(np.mean([p.get("quote_count", 0) for p in posts_data]))
        
        # Fake engagement proxy
        total_engagements = sum(likes) + sum([p.get("reply_count", 0) for p in posts_data]) + sum([p.get("repost_count", 0) for p in posts_data])
        features['engagement_rate'] = (total_engagements / n_posts) / max(features['followers_count'], 1.0)
        features['engagement_variance'] = float(np.std(likes)) if len(likes) > 1 else 0.0
        
        # Content
        texts = [p.get("text", "") for p in posts_data]
        features['average_text_length'] = float(np.mean([len(t) for t in texts]))
        unique_texts = set(t for t in texts if len(t) > 5) # Ignore short "yes", "no"
        features['duplicate_content_ratio'] = 1.0 - (len(unique_texts) / max(len([t for t in texts if len(t) > 5]), 1))
        
        features['hashtag_frequency'] = sum(len(p.get("hashtags", [])) for p in posts_data) / n_posts
        features['mention_frequency'] = sum(len(p.get("mentions", [])) for p in posts_data) / n_posts
        features['url_frequency'] = sum(len(p.get("urls", [])) for p in posts_data) / n_posts
        
        # Repeated hashtags
        all_hashtags = [h for p in posts_data for h in p.get("hashtags", [])]
        if all_hashtags:
            unique_hashtags = set(all_hashtags)
            features['repeated_hashtag_ratio'] = 1.0 - (len(unique_hashtags) / len(all_hashtags))
            
    # Ensure exact feature order for model input
    # Only keep expected features, and in the right order
    final_features = {f: features.get(f, 0.0) for f in EXPECTED_FEATURES}
    return final_features

def validate_features(features: Dict[str, Any]) -> bool:
    """Ensure features match exactly the schema."""
    return list(features.keys()) == EXPECTED_FEATURES
