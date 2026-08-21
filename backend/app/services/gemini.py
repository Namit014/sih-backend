import json
from google import genai
from typing import Dict, Any, Optional
from app.core.config import settings

def explain_risk(risk_data: Dict[str, Any]) -> Optional[str]:
    if not settings.GEMINI_API_KEY:
        return None
        
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        prompt = f"""
        You are an explanation layer for an X (Twitter) Account Risk Detection system.
        The machine learning model has evaluated an account and returned the following structured data:
        
        {json.dumps(risk_data, indent=2)}
        
        Task:
        Provide a concise, human-readable summary explaining what these signals mean and why they contributed to the risk score.
        
        CRITICAL RULES:
        1. NEVER definitively state that the account is "fake". Use cautious language (e.g., "shows anomalous behavior", "exhibits suspicious patterns").
        2. DO NOT invent any signals or data that are not present in the JSON above.
        3. Clarify that the score is based on behavioral patterns and does not independently prove the account is fake.
        4. Keep the explanation to a single short paragraph.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        # If Gemini fails, we silently return None so the API still works without explanation
        return None
