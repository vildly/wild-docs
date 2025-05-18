from typing import List, Dict
import httpx
from app.core.config import settings
import json
import numpy as np
from qdrant_client import QdrantClient
import logging
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.vectordb.qdrant import Qdrant
from agno.embedder.openai import OpenAIEmbedder
from agno.document import Document
from agno.knowledge.url import UrlKnowledge
from agno.tools.reasoning import ReasoningTools

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, api_key: str = None):

        if api_key is None:
            api_key = "sk.."

        # Initialize OpenAI model for the agent
        self.model = OpenAIChat(
            api_key=api_key,
            id="gpt-4-turbo-preview"
        )
        
        # Initialize embedder
        self.embedder = OpenAIEmbedder(
            api_key=api_key,
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
        
        # Initialize knowledge base
        self.knowledge = UrlKnowledge(
            urls=[],  # We'll add URLs dynamically
            vector_db=self.vector_db
        )
        
        # Initialize Agno agent
        self.agent = Agent(
            name="Docs Assistant",
            model=self.model,
            description="""You are a documentation assistant that helps users understand code repositories by analyzing their README files.
            Your goal is to provide clear, accurate, and well-structured answers based on the repository documentation.
            You can search through the documentation to find relevant information and provide comprehensive responses.""",
            instructions=[
                "When answering questions:",
                "1. Focus on explaining the project's purpose, features, and technical details from the documentation",
                "2. Use code blocks when referencing specific code examples or commands",
                "3. Include relevant section titles and links to the source documentation",
                "4. If the documentation is unclear or incomplete, acknowledge the limitations",
                "5. Format your response in clear, readable markdown",
                "6. Always cite your sources by referencing the specific sections you used"
            ],
            knowledge=self.knowledge,
            tools=[ReasoningTools(add_instructions=True)],
            add_datetime_to_instructions=True,
            markdown=True,
            show_tool_calls=True,
            read_chat_history=True
        )

    async def search_similar_chunks(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for similar document chunks using the query embedding"""
        try:
            # Search for similar documents
            results = await self.vector_db.async_search(
                query=query,
                limit=limit
            )
            
            return [
                {
                    "content": doc.content,
                    "title": doc.meta_data["title"],
                    "url": doc.meta_data["url"],
                    "score": doc.meta_data.get("score", 0.0)
                }
                for doc in results
            ]
        except Exception as e:
            logger.error(f"Error searching chunks: {str(e)}")
            return []

    def query_docs(self, query: str) -> Dict:
        """Main method to query documents and get a response"""
        try:
            # Use Agno to generate response
            response = self.agent.run(
                query,
                stream=False
            )
            
            # Extract sources from the response metadata
            sources = []
            if hasattr(response, 'extra_data') and hasattr(response.extra_data, 'references'):
                for ref in response.extra_data.references:
                    for source in ref.references:
                        sources.append({
                            "title": source["meta_data"]["title"],
                            "url": source["meta_data"]["url"],
                            "content": source["content"][:200] + "..." if len(source["content"]) > 200 else source["content"]
                        })
            
            # Create a structured response for the frontend
            return {
                "status": "success",
                "data": {
                    "answer": str(response.content) if hasattr(response, 'content') else str(response),
                    "sources": sources,
                    "metadata": {
                        "model": response.model if hasattr(response, 'model') else None,
                        "run_id": response.run_id if hasattr(response, 'run_id') else None
                    }
                }
            }
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "status": "error",
                "data": {
                    "answer": "I encountered an error while processing your query.",
                    "sources": [],
                    "metadata": {},
                    "error": str(e)
                }
            } 