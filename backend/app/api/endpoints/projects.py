from fastapi import APIRouter, HTTPException
from typing import List
from app.services.document_service import DocumentService
from app.models.project import Project

router = APIRouter()
document_service = DocumentService()

@router.get("", response_model=List[Project])
@router.get("/", response_model=List[Project])
async def list_projects():
    try:
        # Get all documents from Qdrant
        results = await document_service.vector_db.async_search(
            query="What is this project about?",
            limit=100  # Get a reasonable number of documents
        )
        
        # Group documents by URL to get unique projects
        projects = {}
        for doc in results:
            url = doc.meta_data.get("url", "")
            if url and url not in projects:
                # Extract repository name from GitHub URL
                # Example URL: https://github.com/username/repo/blob/main/README.md
                parts = url.split("/")
                if len(parts) >= 5:
                    repo_name = parts[4]  # Get the repository name
                    # Create a link to the repository instead of the README
                    repo_url = f"https://github.com/{parts[3]}/{repo_name}"
                    
                    projects[url] = Project(
                        name=repo_name,
                        readmeUrl=repo_url,
                        description=f"GitHub Repository: {repo_name}"
                    )
        
        return list(projects.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 