from pydantic_settings import BaseSettings, SettingsConfigDict

import os
from pathlib import Path
env_path = Path(__file__).parent.parent.parent / ".env"

class Settings(BaseSettings):
    X_BEARER_TOKEN: str = ""
    GEMINI_API_KEY: str = ""
    
    # ML Thresholds
    RISK_THRESHOLD_MODERATE: int = 25
    RISK_THRESHOLD_SUSPICIOUS: int = 50
    RISK_THRESHOLD_HIGH: int = 75

    model_config = SettingsConfigDict(env_file=str(env_path), env_file_encoding="utf-8", extra="ignore")

settings = Settings()
print("DEBUG - Loading from:", env_path)
print("DEBUG - Token loaded:", bool(settings.X_BEARER_TOKEN))
