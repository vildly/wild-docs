from fastapi import APIRouter, HTTPException
from typing import List
from app.services.document_service import DocumentService
from pydantic import BaseModel, HttpUrl

router = APIRouter()
document_service = DocumentService()

class GitHubRepoRequest(BaseModel):
    repo_url: HttpUrl

class ProcessResponse(BaseModel):
    success: bool
    message: str

@router.post("/process-github", response_model=ProcessResponse)
async def process_github_repo(request: GitHubRepoRequest):
    """Process a GitHub repository's README.md"""
    success = await document_service.process_github_repo(str(request.repo_url))
    if success:
        return ProcessResponse(
            success=True,
            message="Repository processed successfully"
        )
    raise HTTPException(
        status_code=400,
        detail="Failed to process repository"
    )

@router.post("/process-multiple", response_model=List[ProcessResponse])
async def process_multiple_repos(repos: List[GitHubRepoRequest]):
    """Process multiple GitHub repositories"""
    results = []
    for repo in repos:
        success = await document_service.process_github_repo(str(repo.repo_url))
        results.append(
            ProcessResponse(
                success=success,
                message="Repository processed successfully" if success else "Failed to process repository"
            )
        )
    return results 