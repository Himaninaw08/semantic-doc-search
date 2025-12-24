# src/app.py
from flask import Flask, request, jsonify, render_template
from src.retriever import Retriever
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")
retriever = Retriever()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.json
    query = data.get("query", "").strip()
    top_k = int(data.get("top_k", 5))
    if not query:
        return jsonify({"error": "Empty query"}), 400
    results = retriever.retrieve(query, top_k=top_k)
    return jsonify({"query": query, "results": results})

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.json
    query = data.get("query", "").strip()
    top_k = int(data.get("top_k", 3))
    if not query:
        return jsonify({"error": "Empty query"}), 400
    try:
        answer = retriever.generate_answer(query, top_k=top_k)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"query": query, "answer": answer})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
