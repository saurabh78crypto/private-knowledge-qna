# Private Knowledge Q&A Backend

This is the backend service for a private knowledge base Q&A system. It allows users to upload text documents (.txt files), which are chunked, embedded, and stored in a vector database. Users can then query the knowledge base with natural language questions, and the system retrieves relevant context to generate answers using an LLM.

The system supports guest-specific isolation, ensuring that uploaded documents and queries are scoped to individual guest IDs.

## Features

- Upload and manage .txt documents per guest.
- Automatic chunking of documents with overlap for better context retention.
- Vector embeddings using pre-trained models.
- Semantic search over the knowledge base.
- Q&A powered by generative AI, with source citations.
- CORS-enabled for easy frontend integration.

## Technologies Used

- Framework: FastAPI (for building the API)
- Server: Uvicorn (ASGI server for running FastAPI)
- Vector Database: Qdrant (for storing and searching embeddings)
- Embeddings: Sentence Transformers (using model: BAAI/bge-small-en-v1.5)
- LLM: Google Gemini (generative AI for Q&A responses)
- Configuration: Pydantic (for settings and validation) and python-dotenv (for environment variables)
- Other Libraries: python-multipart (for file uploads), and various utilities for chunking, validation, and JSON handling.

## Prerequisites

- Python 3.10 or higher
- A Qdrant instance (cloud or local) with API key and URL
- A Google Gemini API key
- Virtual environment tool (e.g., venv)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/saurabh78crypto/private-knowledge-qna.git
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
On Windows: venv\Scripts\activate
On macOS/Linux: source venv/bin/activate
```

4. Install dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```ts
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_URL=your-qdrant-url (e.g., https://your-qdrant-instance.com)
COLLECTION_NAME=your-collection-name (default: knowledge_base)
GEMINI_API_KEY=your-gemini-api-key
```
- Replace placeholders with your actual credentials.
- Optional settings (configurable in app/config.py): CHUNK_SIZE, CHUNK_OVERLAP, TOP_K, SCORE_THRESHOLD.


## Running the Application

1. Ensure the virtual environment is activated.

2. Start the server:
```bash
python main.py
```
- The server runs on http://0.0.0.0:8000 (or the port specified in PORT env var, default 8000).
- Use --reload for development (enabled by default in the code).

3. Access the API docs:
- Open http://localhost:8000/docs in your browser for Swagger UI.


## API Endpoints

All endpoints require a guest_id query parameter for user isolation.

### Documents

- POST /documents/upload
    - Upload one or more .txt files.
    - Parameters: guest_id (query), files (form data, list of files).
    - Response: Success message with count of uploaded documents.
    - Note: Only .txt files are supported; files are chunked and stored in Qdrant.

- GET /documents
    - List unique documents for a guest.
    - Parameters: guest_id (query).
    - Response: List of documents with IDs, names, and upload timestamps.


### Q&A

- POST /qa/ask
    - Ask a question against the guest's knowledge base.
    - Parameters: guest_id (query).
    - Body: JSON with question field (e.g., { "question": "What is the capital of France?" }).
    - Response: JSON with answer (generated response) and sources (list of document excerpts supporting the answer).
    - If no relevant info, returns a fallback message.

### Configuration Notes

- Chunking: Documents are split into chunks of ~460 tokens with 80-token overlap (configurable).
- Search: Retrieves top-K (default 10) results with score threshold (default 0.0).
- LLM Prompting: Uses Gemini to generate answers strictly from context, with exact excerpts for sources.
- Error Handling: Validates inputs (e.g., guest_id, files, questions) and raises HTTP exceptions for issues.