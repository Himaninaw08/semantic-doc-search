# src/vector_store.py
import numpy as np
import json
from typing import List, Dict

VECTORS_PATH = "data/vectors.npz"
META_PATH = "data/docs_metadata.json"

class VectorStore:
    def __init__(self, vectors_path=VECTORS_PATH, meta_path=META_PATH):
        self.vectors_path = vectors_path
        self.meta_path = meta_path
        self._load()

    def _load(self):
        try:
            data = np.load(self.vectors_path, allow_pickle=True)
            self.embeddings = data["embeddings"]
            self.ids = data["ids"].tolist()
        except Exception:
            self.embeddings = None
            self.ids = []
        try:
            with open(self.meta_path, "r", encoding="utf-8") as f:
                self.meta = json.load(f)
        except Exception:
            self.meta = {}  # id -> {title, text}

    def save(self):
        np.savez_compressed(self.vectors_path, embeddings=self.embeddings, ids=np.array(self.ids, dtype=object))
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def upsert(self, ids: List[str], embeddings, metadatas: List[Dict]):
        # embeddings: np.ndarray (n, dim)
        if self.embeddings is None:
            self.embeddings = embeddings
            self.ids = ids.copy()
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
            self.ids.extend(ids)
        for _id, md in zip(ids, metadatas):
            self.meta[_id] = md
        self.save()

    def search(self, query_embedding, top_k=5):
        # query_embedding: np.ndarray (dim,) or (1,dim)
        if self.embeddings is None or len(self.ids) == 0:
            return []
        q = query_embedding.reshape(1, -1)
        # cosine similarity because embeddings are normalized
        sims = (self.embeddings @ q.T).squeeze()  # shape (n,)
        idx = np.argsort(-sims)[:top_k]
        results = []
        for i in idx:
            _id = self.ids[i]
            results.append({"id": _id, "score": float(sims[i]), "metadata": self.meta[_id]})
        return results
