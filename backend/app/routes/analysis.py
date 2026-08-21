from fastapi import APIRouter, HTTPException, status
from urllib.parse import urlparse

from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AccountInfo, RiskScore
from app.services.x_api import get_user_by_username, get_user_posts, XAPIError
from app.services.feature_engineering import extract_features, validate_features
from app.services.ml_model import predict_risk
from app.services.gemini import explain_risk
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def extract_username(request: AnalysisRequest) -> str:
    if request.username:
        # Strip potential '@' symbol
        return request.username.lstrip('@')
    elif request.profile_url:
        path = urlparse(str(request.profile_url)).path
        parts = path.strip('/').split('/')
        if parts:
            return parts[0]
    raise HTTPException(status_code=400, detail="Must provide either username or profile_url")

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_account(request: AnalysisRequest):
    username = extract_username(request)
    
    try:
        # 1 & 2. Get User and Posts from X API
        user_data = await get_user_by_username(username)
        posts_data = await get_user_posts(user_data["id"])
        
        # 3. Feature Engineering
        features = extract_features(user_data, posts_data)
        
        if not validate_features(features):
            logger.error("Feature mismatch detected during extraction.")
            raise HTTPException(status_code=500, detail="Internal ML feature schema mismatch")
            
        # 4. ML Inference
        try:
            risk_info, signals = predict_risk(features)
        except RuntimeError as e:
            logger.error(f"ML Model error: {e}")
            raise HTTPException(status_code=503, detail="ML model unavailable")
            
        # 5. Optional Gemini Explanation
        explanation = explain_risk({
            "risk_score": risk_info["score"],
            "risk_level": risk_info["level"],
            "signals": signals
        })
        
        # 6. Construct Response
        return AnalysisResponse(
            account=AccountInfo(
                id=user_data["id"],
                username=user_data["username"],
                name=user_data["name"],
                description=user_data.get("description"),
                created_at=user_data["created_at"],
                profile_image_url=user_data.get("profile_image_url"),
                followers=user_data["followers_count"],
                following=user_data["following_count"],
                posts=user_data["post_count"],
                verified=user_data["verified"]
            ),
            risk=RiskScore(**risk_info),
            signals=signals,
            features=features,
            explanation=explanation
        )
        
    except XAPIError as e:
        logger.error(f"XAPIError caught: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error analyzing {username}: {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
