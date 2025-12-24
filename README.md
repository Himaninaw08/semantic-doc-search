# SemanticDocSearch

SemanticDocSearch is a local Retrieval-Augmented-Generation (RAG)-style semantic document search engine. It enables semantic (meaning-based) search over documents using sentence embeddings and a simple file-based vector store. Optionally supports local answer generation using a Hugging Face seq2seq model.

## Features
- Embed documents with `sentence-transformers` (default: `all-MiniLM-L6-v2`)
- Store vectors in `data/vectors.npz` and metadata in `data/docs_metadata.json`
- Fast cosine-similarity retrieval
- Lightweight Flask web UI for search
- Optional local generation using `transformers` (e.g., `flan-t5-small`)

## Quickstart (local)
1. Create venv and install:
   ```bash
   conda create -n myproject python=3.12
   conda activate myproject
   conda install scikit-learn pandas numpy flask
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   *Skip `transformers` & `torch` if you don't need generation.*

2. Generate sample data:
   ```bash
   python utils/dataset_generator.py
   ```

3. Ingest documents (compute embeddings):
   ```bash
   python -m src.ingest
   ```

4. Run the app:
   ```bash
   python -m src.app
   ```
   Visit `http://localhost:5000/`.

## Files
- `src/` — core Python modules (embedder, vector store, retriever, flask app)
- `templates/` and `static/` — frontend
- `data/` — sample dataset and generated vectors/metadata
- `utils/` — helper scripts (dataset generator)

## Notes & Extensions
- Replace CSV input with PDF/Word parsing for real datasets.
- Swap embedding model by setting `EMBED_MODEL` environment var.
- For large datasets, replace file-based store with FAISS or Milvus for speed / memory.
- For answer synthesis, install `transformers` and `torch` and set model in `retriever.generate_answer`.

## License
MIT. See LICENSE file.
