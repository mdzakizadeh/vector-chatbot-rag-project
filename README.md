# Vector Chatbot (RAG)

This project is a minimal Retrieval-Augmented Generation (RAG) chatbot:
- Extracts text from PDFs
- Chunks text into smaller passages
- Generates embeddings with Ollama
- Stores vectors in Qdrant
- Answers questions via FastAPI

## Quickstart
1. Start Qdrant:
   docker run -p 6333:6333 qdrant/qdrant
2. Install Python dependencies:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
3. Run API:
   uvicorn app.main:app --reload --port 8000
4. Ingest PDF and query
