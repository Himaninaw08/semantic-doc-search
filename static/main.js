// static/main.js
async function search() {
  const q = document.getElementById("query").value;
  const topk = document.getElementById("topk").value;
  document.getElementById("results").innerHTML = "<em>Searching…</em>"
  const res = await fetch("/api/search", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({query: q, top_k: topk})
  });
  const data = await res.json();
  if (data.error) {
    document.getElementById("results").innerHTML = `<div style="color:red">${data.error}</div>`;
    return;
  }
  const html = data.results.map(r => {
    return `<div class="doc">
      <div><strong>${r.metadata.title}</strong></div>
      <div class="score">score: ${r.score.toFixed(4)}</div>
      <div style="margin-top:6px">${r.metadata.text}</div>
    </div>`;
  }).join("");
  document.getElementById("results").innerHTML = html || "<div>No results</div>";
}

async function generate() {
  const q = document.getElementById("query").value;
  const topk = document.getElementById("topk").value;
  document.getElementById("results").innerHTML = "<em>Generating answer…</em>"
  const res = await fetch("/api/generate", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({query: q, top_k: topk})
  });
  const data = await res.json();
  if (data.error) {
    document.getElementById("results").innerHTML = `<div style="color:red">${data.error}</div>`;
    return;
  }
  const html = `<div class="doc"><strong>Answer:</strong><div style="margin-top:8px">${data.answer}</div></div>`;
  document.getElementById("results").innerHTML = html;
}
