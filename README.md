# Wild Docs

Wild Docs is an AI-powered documentation assistant that helps users understand code repositories by analyzing their README files and documentation. It uses OpenAI's GPT models to provide clear, accurate, and well-structured answers based on the repository documentation.

## Features
- Analyze GitHub repositories and their documentation
- Interactive chat interface for asking questions about the codebase
- Semantic search through documentation
- Source citation and references
- Support for multiple projects

## Tech Stack
- Frontend: Next.js with TypeScript
- Backend: FastAPI (Python)
- Vector Database: Qdrant for semantic search
- AI: OpenAI GPT-4 and Embeddings
- Containerization: Docker

## Running the Application

### Development Mode
To run the application in development mode:
```bash
docker-compose -f docker-compose.dev.yml up
```

This will start the services with:
- Frontend in development mode with hot reloading
- Backend with development settings
- Qdrant vector database

### Production Mode
To run the application in production mode:
```bash
docker-compose -f docker-compose.prod.yml up
```

This will start the services with:
- Frontend in production mode
- Backend with production settings
- Qdrant vector database

### Environment Variables
Make sure to set the following environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key

### Ports
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Qdrant: http://localhost:6333 