from fastapi import APIRouter, HTTPException
from typing import List
from app.services.project_service import ProjectService, Project
from app.services.document_service import DocumentService
from app.api.deps import get_openai_api_key
from app.core.config import settings

router = APIRouter()
project_service = ProjectService()

@router.get("/", response_model=List[Project])
async def list_projects():
    """Get all projects"""
    try:
        return project_service.get_projects()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
async def add_project(repo_url: str, api_key: str = settings.OPENAI_API_KEY):
    """Add a new project and process its documentation"""
    try:
        # Process the repository documentation
        document_service = DocumentService(api_key=api_key)
        await document_service.process_github_repo(repo_url)
        
        # Extract repository name from GitHub URL
        # Example URL: https://github.com/username/repo/blob/main/README.md
        parts = repo_url.split("/")
        if len(parts) >= 5:
            repo_name = parts[4]  # Get the repository name
            # Create a link to the repository instead of the README
            repo_url = f"https://github.com/{parts[3]}/{repo_name}"
            
            # Add project to our storage
            project = project_service.add_project(
                name=repo_name,
                readmeUrl=repo_url,
                description=f"GitHub Repository: {repo_name}"
            )
            
            return {"status": "success", "project": project}
        else:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 