# src/retriever.py
from src.embedder import Embedder
from src.vector_store import VectorStore
import numpy as np

# Optional imports for local generation
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
    HF_AVAILABLE = True
except Exception:
    HF_AVAILABLE = False

class Retriever:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embedder = Embedder(model_name)
        self.store = VectorStore()
        self.gen_pipeline = None

    def retrieve(self, query: str, top_k=5):
        q_emb = self.embedder.encode([query])[0]
        results = self.store.search(q_emb, top_k=top_k)
        return results

    def generate_answer(self, query: str, top_k=3, model_name="google/flan-t5-small", max_length=200):
        """
        Optionally synthesize an answer using a local HF model.
        This is optional and only works if transformers & torch are installed.
        """
        if not HF_AVAILABLE:
            raise RuntimeError("Transformers not available. Install transformers and torch to generate answers.")
        # build prompt with query + retrieved passages
        retrieved = self.retrieve(query, top_k=top_k)
        context = "\n\n".join([f"Title: {r['metadata']['title']}\nText: {r['metadata']['text']}" for r in retrieved])
        prompt = f"Use the following context to answer the question. If the answer is not contained, say 'I don't know'.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
        # lazy-load pipeline
        if self.gen_pipeline is None:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.gen_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=-1)
        out = self.gen_pipeline(prompt, max_length=max_length, do_sample=False)
        return out[0]["generated_text"]
