# src/embedder.py
from sentence_transformers import SentenceTransformer
import numpy as np
import os

MODEL_NAME = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")

class Embedder:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, show_progress_bar=False):
        # Returns numpy array (n_docs, dim)
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=show_progress_bar)
        # l2-normalize for cosine similarity speed up
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        embeddings = embeddings / norms
        return embeddings
