from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import ChatService
from typing import List, Dict, Optional

router = APIRouter()
chat_service = ChatService()

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

@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    """Query the documents and get a response"""
    try:
        result = chat_service.query_docs(request.query)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        ) 