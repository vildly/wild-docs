from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.chat_service import ChatService
from typing import List, Dict, Optional
from app.api.deps import get_openai_api_key

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class Source(BaseModel):
    title: str
    url: str
    content: str

class Metadata(BaseModel):
    model: Optional[str] = None
    run_id: Optional[str] = None

class QueryResponseData(BaseModel):
    answer: str
    sources: List[Source]
    metadata: Metadata

class QueryResponse(BaseModel):
    status: str
    data: QueryResponseData

class ChatRequest(BaseModel):
    message: str

@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    """Query the documents and get a response"""
    try:
        api_key = get_openai_api_key()
        chat_service = ChatService(api_key=api_key)
        result = chat_service.query_docs(request.query)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@router.post("/chat")
async def chat(request: ChatRequest, api_key: str = Depends(get_openai_api_key)):
    chat_service = ChatService(api_key=api_key)
    response = chat_service.query_docs(request.message)
    return response 