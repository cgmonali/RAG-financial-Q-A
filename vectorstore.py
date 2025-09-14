import faiss
import numpy as np
from typing import List, Dict
from .embeddings import get_embedding

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.vectors = []
        self.metadata = []

    def add(self, embedding: List[float], meta: Dict):
        vec = np.array([embedding], dtype="float32")
        self.index.add(vec)
        self.vectors.append(embedding)
        self.metadata.append(meta)

    def search(self, query: str, top_k: int = 3):
        try:
            q_emb = np.array([get_embedding(query, input_type="search_query")], dtype="float32")
        except Exception as e:
            print(f"[ERROR] Failed to embed query: {e}")
            return []

        D, I = self.index.search(q_emb, top_k)
        results = []
        for idx in I[0]:
            if 0 <= idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results
