import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import markdown
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.config import settings
import logging
import uuid
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.vectordb.qdrant import Qdrant
from agno.embedder.openai import OpenAIEmbedder
from agno.document import Document
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        try:
            # Initialize OpenRouter model for the agent
            self.model = OpenRouter(
                base_url="https://api.openrouter.ai/api/v1",
                api_key=settings.OPENROUTER_API_KEY,
                id="anthropic/claude-3-haiku"
            )
            
            # Initialize embedder
            self.embedder = OpenAIEmbedder(
                api_key=settings.OPENAI_API_KEY,
                id="text-embedding-3-small", 
                dimensions=1536
            )
            
            # Initialize Qdrant client
            self.qdrant_client = QdrantClient(url=settings.QDRANT_URL)
            
            # Initialize Agno vector store
            self.vector_db = Qdrant(
                collection=settings.QDRANT_COLLECTION_NAME,
                embedder=self.embedder,
                url=settings.QDRANT_URL
            )
            
            # Ensure collection exists
            self._ensure_collection()
            
        except Exception as e:
            logger.error(f"Failed to initialize services: {e}")
            raise

    def _ensure_collection(self):
        """Ensure the Qdrant collection exists with proper configuration"""
        try:
            if not self.vector_db.exists():
                logger.info(f"Creating collection: {settings.QDRANT_COLLECTION_NAME}")
                self.vector_db.create()
        except Exception as e:
            logger.error(f"Failed to ensure collection exists: {e}")
            raise

    async def fetch_github_markdown(self, url: str) -> str:
        """Fetch markdown content from a GitHub URL."""
        try:
            # Convert GitHub URL to raw content URL
            # Example: https://github.com/username/repo/blob/main/README.md
            # to: https://raw.githubusercontent.com/username/repo/main/README.md
            url_parts = url.split('/')
            if 'github.com' in url_parts:
                # Find the index of 'github.com'
                github_index = url_parts.index('github.com')
                # Get the parts after github.com
                path_parts = url_parts[github_index + 1:]
                
                # Remove 'blob' if it exists
                if 'blob' in path_parts:
                    blob_index = path_parts.index('blob')
                    path_parts.pop(blob_index)  # Remove 'blob'
                
                # Construct the raw URL
                raw_url = f"https://raw.githubusercontent.com/{'/'.join(path_parts)}"
                logger.info(f"Fetching markdown from: {raw_url}")
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(raw_url) as response:
                        if response.status == 200:
                            return await response.text()
                        else:
                            logger.error(f"Error fetching markdown: {response.status} {response.reason} for url: {raw_url}")
                            raise Exception(f"Failed to fetch markdown content: {response.status} {response.reason}")
        except Exception as e:
            logger.error(f"Error fetching markdown: {str(e)}")
            raise Exception(f"Failed to fetch markdown content: {str(e)}")

    def process_markdown(self, content: str) -> List[Dict]:
        """Process markdown content into chunks for embedding"""
        try:
            # Convert markdown to HTML
            html = markdown.markdown(content)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Split into sections (h1, h2, h3 headers)
            sections = []
            current_section = {"title": "", "content": ""}
            
            for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
                if element.name in ['h1', 'h2', 'h3']:
                    if current_section["content"]:
                        sections.append(current_section)
                    current_section = {
                        "title": element.get_text(),
                        "content": element.get_text()
                    }
                else:
                    current_section["content"] += "\n" + element.get_text()
            
            if current_section["content"]:
                sections.append(current_section)
            
            logger.info(f"Processed markdown into {len(sections)} sections")
            return sections
        except Exception as e:
            logger.error(f"Error processing markdown: {e}")
            raise

    async def store_document(self, url: str, content: str):
        """Store processed document in Qdrant"""
        try:
            logger.info("Processing markdown into sections")
            sections = self.process_markdown(content)
            logger.info(f"Created {len(sections)} sections")
            
            for i, section in enumerate(sections):
                logger.info(f"Processing section {i+1}/{len(sections)}")
                try:
                    logger.info("Storing section in Qdrant")
                    # Create Agno Document
                    doc = Document(
                        name=f"section_{i}",
                        content=section["content"],
                        meta_data={
                            "url": url,
                            "title": section["title"],
                            "type": "markdown"
                        }
                    )
                    
                    # Insert document
                    await self.vector_db.async_insert([doc])
                    logger.info("Successfully stored section")
                except Exception as e:
                    logger.error(f"Error processing section {i+1}: {str(e)}")
                    logger.exception("Full traceback:")
                    raise
            
            logger.info(f"Stored document from {url} with {len(sections)} sections")
        except Exception as e:
            logger.error(f"Error storing document: {str(e)}")
            logger.exception("Full traceback:")
            raise

    async def process_github_repo(self, repo_url: str):
        """Process a GitHub repository's README.md"""
        try:
            # If the URL already contains 'blob/main/README.md', use it as is
            if 'blob/main/README.md' in repo_url:
                readme_url = repo_url
            else:
                # Remove trailing slash if present
                repo_url = repo_url.rstrip('/')
                # Construct the README URL
                readme_url = f"{repo_url}/blob/main/README.md"
            
            logger.info(f"Processing GitHub repo: {readme_url}")
            content = await self.fetch_github_markdown(readme_url)
            if content:
                logger.info("Successfully fetched markdown content")
                await self.store_document(readme_url, content)
                return True
            logger.error("Failed to fetch markdown content")
            return False
        except Exception as e:
            logger.error(f"Error processing GitHub repo: {str(e)}")
            logger.exception("Full traceback:")
            raise 