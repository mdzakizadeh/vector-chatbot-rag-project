from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uuid
from .ingest import extract_text_from_pdf, chunk_text
from .embeddings import get_embedding
from .qdrant_store import QdrantStore
from .retriever import Retriever
import ollama

app = FastAPI(title="Vector-RAG Chatbot")
qstore = QdrantStore()
retriever = Retriever(qstore)

class QueryIn(BaseModel):
    question: str

@app.post("/ingest_pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    content = await file.read()
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(content)
    text = extract_text_from_pdf(path)
    chunks = chunk_text(text)
    vectors, metadatas, ids = [], [], []
    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        vectors.append(emb)
        metadatas.append({"text": chunk, "source": file.filename})
        ids.append(str(uuid.uuid4()))
    qstore.upsert(vectors, metadatas, ids)
    return {"status": "ok", "chunks": len(chunks)}

@app.post("/query")
async def query(q: QueryIn):
    hits = retriever.retrieve(q.question, top_k=4)
    context = "\n\n---\n\n".join([h["text"] for h in hits])
    prompt = f"You are a helpful assistant. Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {q.question}\n\nAnswer concisely and cite sources by filename."
    resp = ollama.generate(model="gemma3", prompt=prompt)
    answer = resp.get("content") if isinstance(resp, dict) else str(resp)
    return {"answer": answer, "sources": [h["id"] for h in hits]}
