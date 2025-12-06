from .embeddings import get_embedding
from .qdrant_store import QdrantStore

class Retriever:
    def __init__(self, qdrant_store: QdrantStore, embed_model="embeddinggemma"):
        self.store = qdrant_store
        self.embed_model = embed_model
    def retrieve(self, query: str, top_k=5):
        v = get_embedding(query, model=self.embed_model)
        hits = self.store.search(v, top_k=top_k)
        results = []
        for h in hits:
            payload = h.get("payload") or {}
            text = payload.get("text") or payload.get("content") or ""
            results.append({"id": h.get("id"), "score": h.get("score"), "text": text})
        return results
