import os
import json
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression

os.makedirs('ml/models', exist_ok=True)

schema = {
    'version': '1.0',
    'features': [
        'account_age_days', 'followers_count', 'following_count', 'post_count', 
        'followers_following_ratio', 'profile_completeness', 'verified',
        'posts_per_day', 'average_post_interval', 'posting_interval_std', 
        'reply_ratio', 'repost_ratio', 'original_post_ratio', 'activity_burst_score',
        'average_likes', 'average_replies', 'average_reposts', 'average_quotes', 
        'engagement_rate', 'engagement_variance',
        'duplicate_content_ratio', 'average_text_length', 'hashtag_frequency', 
        'mention_frequency', 'url_frequency', 'repeated_hashtag_ratio'
    ]
}

with open('ml/models/feature_schema.json', 'w') as f:
    json.dump(schema, f, indent=4)

# Create a dummy model
X = pd.DataFrame([[0.0] * len(schema['features']), [1.0] * len(schema['features'])], columns=schema['features'])
y = [0, 1]
model = LogisticRegression().fit(X, y)
joblib.dump(model, 'ml/models/x_account_risk_model.pkl')
joblib.dump(model, 'ml/models/x_account_risk_model.pkl')

print("Dummy model and schema created.")
