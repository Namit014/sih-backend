import pandas as pd
import numpy as np

np.random.seed(42)
n_samples = 500

# Legitimate accounts
n_legit = int(n_samples * 0.8)
legit_data = {
    'account_id': np.arange(1, n_legit + 1),
    'account_age_days': np.random.randint(365, 3650, n_legit),
    'followers_count': np.random.randint(100, 10000, n_legit),
    'following_count': np.random.randint(50, 2000, n_legit),
    'post_count': np.random.randint(500, 50000, n_legit),
    'profile_completeness': np.random.uniform(0.7, 1.0, n_legit),
    'verified': np.random.choice([0, 1], p=[0.9, 0.1], size=n_legit),
    
    'posts_per_day': np.random.uniform(0.5, 5.0, n_legit),
    'average_post_interval': np.random.uniform(4, 48, n_legit),
    'posting_interval_std': np.random.uniform(2, 24, n_legit),
    'reply_ratio': np.random.uniform(0.1, 0.6, n_legit),
    'repost_ratio': np.random.uniform(0.05, 0.4, n_legit),
    'original_post_ratio': np.random.uniform(0.1, 0.8, n_legit),
    'activity_burst_score': np.random.uniform(1.0, 3.0, n_legit),
    
    'average_likes': np.random.uniform(5, 500, n_legit),
    'average_replies': np.random.uniform(1, 50, n_legit),
    'average_reposts': np.random.uniform(0, 100, n_legit),
    'average_quotes': np.random.uniform(0, 20, n_legit),
    'engagement_rate': np.random.uniform(0.01, 0.1, n_legit),
    'engagement_variance': np.random.uniform(0.1, 2.0, n_legit),
    
    'duplicate_content_ratio': np.random.uniform(0.0, 0.05, n_legit),
    'average_text_length': np.random.uniform(40, 200, n_legit),
    'hashtag_frequency': np.random.uniform(0.1, 1.0, n_legit),
    'mention_frequency': np.random.uniform(0.2, 1.5, n_legit),
    'url_frequency': np.random.uniform(0.05, 0.5, n_legit),
    'repeated_hashtag_ratio': np.random.uniform(0.0, 0.1, n_legit),
    
    'label': np.zeros(n_legit, dtype=int)
}

# Suspicious accounts
n_suspicious = n_samples - n_legit
suspicious_data = {
    'account_id': np.arange(n_legit + 1, n_samples + 1),
    'account_age_days': np.random.randint(1, 180, n_suspicious),
    'followers_count': np.random.randint(0, 500, n_suspicious),
    'following_count': np.random.randint(1000, 5000, n_suspicious),
    'post_count': np.random.randint(100, 10000, n_suspicious),
    'profile_completeness': np.random.uniform(0.1, 0.6, n_suspicious),
    'verified': np.zeros(n_suspicious, dtype=int),
    
    'posts_per_day': np.random.uniform(10.0, 50.0, n_suspicious),
    'average_post_interval': np.random.uniform(0.5, 3.0, n_suspicious),
    'posting_interval_std': np.random.uniform(0.1, 1.0, n_suspicious),
    'reply_ratio': np.random.uniform(0.5, 0.95, n_suspicious),
    'repost_ratio': np.random.uniform(0.4, 0.9, n_suspicious),
    'original_post_ratio': np.random.uniform(0.0, 0.2, n_suspicious),
    'activity_burst_score': np.random.uniform(5.0, 15.0, n_suspicious),
    
    'average_likes': np.random.uniform(0, 5, n_suspicious),
    'average_replies': np.random.uniform(0, 2, n_suspicious),
    'average_reposts': np.random.uniform(0, 2, n_suspicious),
    'average_quotes': np.random.uniform(0, 1, n_suspicious),
    'engagement_rate': np.random.uniform(0.0, 0.005, n_suspicious),
    'engagement_variance': np.random.uniform(0.0, 0.1, n_suspicious),
    
    'duplicate_content_ratio': np.random.uniform(0.3, 0.9, n_suspicious),
    'average_text_length': np.random.uniform(10, 80, n_suspicious),
    'hashtag_frequency': np.random.uniform(1.0, 5.0, n_suspicious),
    'mention_frequency': np.random.uniform(1.0, 4.0, n_suspicious),
    'url_frequency': np.random.uniform(0.5, 2.0, n_suspicious),
    'repeated_hashtag_ratio': np.random.uniform(0.4, 0.9, n_suspicious),
    
    'label': np.ones(n_suspicious, dtype=int)
}

# calculate derived feature for both
for d in [legit_data, suspicious_data]:
    d['followers_following_ratio'] = d['followers_count'] / np.maximum(d['following_count'], 1)

df_legit = pd.DataFrame(legit_data)
df_suspicious = pd.DataFrame(suspicious_data)

df_combined = pd.concat([df_legit, df_suspicious]).sample(frac=1, random_state=42).reset_index(drop=True)
df_combined.to_csv('ml/dataset/accounts.csv', index=False)
print("Dataset generated at ml/dataset/accounts.csv")
