from pydantic import BaseModel

class Project(BaseModel):
    name: str
    readmeUrl: str
    description: str 