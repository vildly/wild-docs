from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.services.document_service import DocumentService
from pydantic import BaseModel, HttpUrl
from app.api.deps import get_openai_api_key
from app.core.config import settings

router = APIRouter()
document_service = DocumentService()

class GitHubRepoRequest(BaseModel):
    repo_url: HttpUrl

class ProcessResponse(BaseModel):
    success: bool
    message: str

class ProcessGitHubRequest(BaseModel):
    repo_url: str

@router.post("/process-github")
async def process_github_repo(request: ProcessGitHubRequest, api_key: str = settings.OPENAI_API_KEY):
    """Process a GitHub repository and store its documentation"""
    try:
        document_service = DocumentService(api_key=api_key)
        result = await document_service.process_github_repo(request.repo_url)
        return {"status": "success", "message": "Repository processed successfully", "data": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing repository: {str(e)}"
        )

class ProcessMultipleRequest(BaseModel):
    repo_urls: List[str]

@router.post("/process-multiple")
async def process_multiple_repos(request: ProcessMultipleRequest, api_key: str = settings.OPENAI_API_KEY):
    """Process multiple GitHub repositories"""
    try:
        document_service = DocumentService(api_key=api_key)
        results = []
        for url in request.repo_urls:
            try:
                result = await document_service.process_github_repo(url)
                results.append({"url": url, "status": "success", "data": result})
            except Exception as e:
                results.append({"url": url, "status": "error", "error": str(e)})
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing repositories: {str(e)}"
        ) 