from fastapi import Header, HTTPException
from typing import Optional

async def get_openai_api_key(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="OpenAI API key not provided. Please set your API key in the settings."
        )
    
    if not authorization.startswith('Bearer '):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Must start with 'Bearer '"
        )
    
    api_key = authorization.replace('Bearer ', '')
    
    if not api_key.startswith('sk-'):
        raise HTTPException(
            status_code=401,
            detail="Invalid OpenAI API key format. Must start with 'sk-'"
        )
    
    return api_key 