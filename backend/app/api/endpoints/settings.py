from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import settings

router = APIRouter()

class APIKeyRequest(BaseModel):
    api_key: str

@router.post("/api-key")
async def store_api_key(request: APIKeyRequest):
    """Store the OpenAI API key"""
    try:
        if not request.api_key.startswith('sk-'):
            raise HTTPException(
                status_code=400,
                detail="Invalid API key format. Must start with 'sk-'"
            )
        
        # Store the API key in settings
        settings.OPENAI_API_KEY = request.api_key
        
        return {"status": "success", "message": "API key stored successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error storing API key: {str(e)}"
        ) 