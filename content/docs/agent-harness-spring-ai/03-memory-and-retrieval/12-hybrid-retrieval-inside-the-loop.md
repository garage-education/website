---
title: "Chapter 12: Hybrid retrieval inside the loop"
linktitle: "12. Hybrid retrieval"
summary: "Vector top 20 and BM25 top 20, merged by Reciprocal Rank Fusion, exposed as a tool that must be cited."
weight: 130

date: "2026-10-10T00:00:00Z"
toc: true
---

Run two searches and merge them. The vector search returns the 20 closest chunks. The keyword search returns the 20 best BM25 matches. Reciprocal Rank Fusion merges the two lists by rank. Each chunk scores the sum of 1 divided by 60 plus its rank in each list.

<figure class="arch">
<script type="application/json">
{
  "title": "Two searches, one fused list.",
  "nodes": [
    {"id": "q", "x": 0, "y": 90, "w": 150, "label": "Search tool call", "detail": "from the model", "tone": "platform"},
    {"id": "vec", "x": 220, "y": 20, "w": 190, "label": "Vector search", "detail": "20 closest chunks", "tone": "data"},
    {"id": "kw", "x": 220, "y": 160, "w": 190, "label": "Keyword search", "detail": "20 best BM25 matches", "tone": "data"},
    {"id": "rrf", "x": 470, "y": 90, "w": 200, "label": "Reciprocal Rank Fusion", "detail": "score = Σ 1 / (60 + rank)", "tone": "platform"},
    {"id": "model", "x": 720, "y": 90, "w": 150, "label": "Model", "detail": "cites each claim", "tone": "ai"}
  ],
  "edges": [
    {"from": "q", "to": "vec", "label": "embed query", "fromSide": "right", "toSide": "left"},
    {"from": "q", "to": "kw", "label": "keywords", "fromSide": "right", "toSide": "left"},
    {"from": "vec", "to": "rrf", "label": "ranks", "fromSide": "right", "toSide": "left"},
    {"from": "kw", "to": "rrf", "label": "ranks", "fromSide": "right", "toSide": "left"},
    {"from": "rrf", "to": "model", "label": "tool result"}
  ]
}
</script>
<figcaption>Figure 12.1. Hybrid retrieval. RRF uses rank positions, not raw scores, so a vector distance and a BM25 score never need to be compared. Chapter 13 adds filters and a reranker.</figcaption>
</figure>

**Worked example of the RRF formula.** A chunk ranked 1st in the vector list and 3rd in the keyword list scores 1/61 + 1/63 ≈ 0.0323. A chunk ranked 2nd in the vector list only scores 1/62 ≈ 0.0161. Appearing in both lists wins.

Expose the merged search as a tool. Require a citation for each claim. If the answer has no citation and does not say no match, send one correction. Stop if it still has none.

<figure class="arch">
<script type="application/json">
{
  "title": "The citation check, with one correction.",
  "nodes": [
    {"id": "ans", "x": 0, "y": 60, "w": 150, "label": "Model answer", "tone": "ai"},
    {"id": "c1", "x": 190, "y": 60, "w": 190, "label": "Cited, or says no match?", "tone": "platform"},
    {"id": "fix", "x": 190, "y": 190, "w": 190, "label": "Send one correction", "tone": "platform"},
    {"id": "c2", "x": 420, "y": 190, "w": 190, "label": "Cited, or says no match?", "tone": "platform"},
    {"id": "ok", "x": 650, "y": 60, "w": 150, "label": "Accept the answer", "tone": "platform"},
    {"id": "stop", "x": 650, "y": 190, "w": 150, "label": "Stop the run", "tone": "muted"}
  ],
  "edges": [
    {"from": "ans", "to": "c1"},
    {"from": "c1", "to": "ok", "label": "yes"},
    {"from": "c1", "to": "fix", "label": "no"},
    {"from": "fix", "to": "c2", "label": "new answer"},
    {"from": "c2", "to": "ok", "label": "yes", "fromSide": "top", "toSide": "bottom"},
    {"from": "c2", "to": "stop", "label": "no"}
  ]
}
</script>
<figcaption>Figure 12.2. One correction, never a second. The chapter does not name the stop reason for an uncited answer.</figcaption>
</figure>
