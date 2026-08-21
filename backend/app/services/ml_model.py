import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Load model globally on startup
MODEL_PATH = "../ml/models/x_account_risk_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    logger.error(f"Failed to load model from {MODEL_PATH}: {e}")
    model = None

def get_risk_level(score: int) -> str:
    if score <= settings.RISK_THRESHOLD_MODERATE:
        return "low"
    elif score <= settings.RISK_THRESHOLD_SUSPICIOUS:
        return "moderate"
    elif score <= settings.RISK_THRESHOLD_HIGH:
        return "suspicious"
    else:
        return "high"

def generate_signals(features: Dict[str, Any]) -> List[str]:
    signals = []
    
    # These thresholds are heuristic and should ideally be calibrated with the dataset
    if features.get('posts_per_day', 0) > 15:
        signals.append("High posting frequency")
        
    if features.get('duplicate_content_ratio', 0) > 0.3:
        signals.append("High repetitive-content ratio")
        
    if features.get('followers_following_ratio', 1) < 0.1 and features.get('following_count', 0) > 100:
        signals.append("Unusual follower/following ratio")
        
    if features.get('reply_ratio', 0) > 0.8:
        signals.append("Account primarily posts replies")
        
    if features.get('account_age_days', 365) < 30:
        signals.append("Recently created account")
        
    if features.get('repeated_hashtag_ratio', 0) > 0.5:
        signals.append("High usage of repeated hashtags")
        
    return signals

def predict_risk(features: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    if model is None:
        raise RuntimeError("ML model is not loaded.")
        
    # Model expects a DataFrame with columns matching the features
    df = pd.DataFrame([features])
    
    # XGBoost output probability for class 1
    prob = float(model.predict_proba(df)[0][1])
    score = int(prob * 100)
    level = get_risk_level(score)
    
    signals = generate_signals(features)
    
    return {
        "score": score,
        "probability": prob,
        "level": level
    }, signals
