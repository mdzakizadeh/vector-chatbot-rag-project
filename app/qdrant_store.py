from qdrant_client import QdrantClient
from qdrant_client.http import models as rest_models
from typing import List, Dict
COLLECTION_NAME = "documents"

class QdrantStore:
    def __init__(self, url="localhost", port=6333, prefer_grpc=False, distance="Cosine", vector_size=384):
        self.client = QdrantClient(host=url, port=port, prefer_grpc=prefer_grpc)
        try:
            self.client.get_collection(collection_name=COLLECTION_NAME)
        except:
            self.client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=rest_models.VectorParams(size=vector_size, distance=rest_models.Distance.COSINE)
            )
    def upsert(self, vectors: List[List[float]], metadatas: List[Dict], ids: List[str]):
        from qdrant_client.models import PointStruct
        points = [PointStruct(id=ids[i], vector=vectors[i], payload=metadatas[i]) for i in range(len(ids))]
        self.client.upsert(collection_name=COLLECTION_NAME, points=points)
    def search(self, vector: List[float], top_k=5):
        res = self.client.search(collection_name=COLLECTION_NAME, query_vector=vector, limit=top_k)
        return [{"id": r.id, "score": r.score, "payload": r.payload} for r in res]
