# src/ingest.py
"""Usage: python -m src.ingest
Reads data/sample_docs.csv (title,text) and builds embeddings + vector store.
"""
import csv
import os
from src.embedder import Embedder
from src.vector_store import VectorStore
from tqdm import tqdm
import uuid

DATA_PATH = "data/sample_docs.csv"

def read_csv(path=DATA_PATH):
    docs = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            title = r.get("title", "").strip()
            text = r.get("text", "").strip()
            if text:
                docs.append({"title": title or text[:40], "text": text})
    return docs

def chunk_doc(text, chunk_size=400, overlap=50):
    # naive token/char chunking (char-based)
    out = []
    start = 0
    while start < len(text):
        chunk = text[start:start+chunk_size]
        out.append(chunk)
        start += chunk_size - overlap
    return out

def main():
    docs = read_csv()
    embedder = Embedder()
    vs = VectorStore()
    ids, embeddings, metas = [], [], []
    for doc in tqdm(docs, desc="Ingesting documents"):
        chunks = chunk_doc(doc["text"], chunk_size=600, overlap=100)
        for i, ch in enumerate(chunks):
            _id = str(uuid.uuid4())
            ids.append(_id)
            metas.append({
                "title": doc["title"],
                "text": ch
            })
    texts = [m["text"] for m in metas]
    if len(texts) == 0:
        print("No texts found in data file.")
        return
    emb = embedder.encode(texts, show_progress_bar=True)
    vs.upsert(ids, emb, metas)
    print(f"Ingested {len(texts)} chunks. Saved vectors to {vs.vectors_path} and metadata to {vs.meta_path}")

if __name__ == "__main__":
    main()
