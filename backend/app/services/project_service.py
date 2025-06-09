import json
import os
import logging
from typing import List, Dict
from pydantic import BaseModel
from pathlib import Path

logger = logging.getLogger(__name__)

class Project(BaseModel):
    name: str
    readmeUrl: str
    description: str

class ProjectService:
    def __init__(self):
        # Create data directory in the app folder
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)  # Creates the data directory if it doesn't exist
        self.projects_file = self.data_dir / "projects.json"
        logger.info(f"Projects file path: {self.projects_file}")
        self._ensure_projects_file()  # Creates the JSON file if it doesn't exist

    def _ensure_projects_file(self):
        """Ensure the projects file exists"""
        if not self.projects_file.exists():
            logger.info("Creating new projects.json file")
            with open(self.projects_file, 'w') as f:
                json.dump([], f)  # Creates an empty JSON array
        else:
            logger.info("Projects file already exists")

    def get_projects(self) -> List[Project]:
        """Get all projects from the JSON file"""
        try:
            logger.info(f"Reading projects from {self.projects_file}")
            with open(self.projects_file, 'r') as f:
                projects_data = json.load(f)
                logger.info(f"Found {len(projects_data)} projects")
                return [Project(**project) for project in projects_data]
        except Exception as e:
            logger.error(f"Error reading projects: {e}")
            return []

    def add_project(self, name: str, readmeUrl: str, description: str) -> Project:
        """Add a new project to the JSON file"""
        try:
            projects = self.get_projects()
            new_project = Project(
                name=name,
                readmeUrl=readmeUrl,
                description=description
            )
            projects.append(new_project)
            
            logger.info(f"Writing {len(projects)} projects to {self.projects_file}")
            with open(self.projects_file, 'w') as f:
                json.dump([project.model_dump() for project in projects], f, indent=2)
                        
            return new_project
        except Exception as e:
            logger.error(f"Error adding project: {e}")
            raise 