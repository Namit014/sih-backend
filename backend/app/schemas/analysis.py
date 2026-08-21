from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any

class AnalysisRequest(BaseModel):
    username: Optional[str] = None
    profile_url: Optional[HttpUrl] = None

class AccountInfo(BaseModel):
    id: str
    username: str
    name: str
    description: Optional[str] = None
    created_at: str
    profile_image_url: Optional[str] = None
    followers: int
    following: int
    posts: int
    verified: bool

class RiskScore(BaseModel):
    score: int
    probability: float
    level: str

class AnalysisResponse(BaseModel):
    account: AccountInfo
    risk: RiskScore
    signals: List[str]
    features: Dict[str, Any]
    explanation: Optional[str] = None
