import ollama
from typing import List

OLLAMA_BASE = "http://localhost:11434"

def get_embedding(text: str, model: str = "embeddinggemma") -> List[float]:
    try:
        resp = ollama.embed(model=model, input=text)
        if isinstance(resp, dict) and "embeddings" in resp:
            return resp["embeddings"][0]
        if isinstance(resp, dict) and "embedding" in resp:
            return resp["embedding"]
        return resp[0]
    except Exception as e:
        import requests
        payload = {"model": model, "input": text}
        r = requests.post("http://localhost:11434/api/embed", json=payload)
        r.raise_for_status()
        data = r.json()
        if "embeddings" in data:
            return data["embeddings"][0]
        if "embedding" in data:
            return data["embedding"]
        return data[0]
