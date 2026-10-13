---
title: "Chapter 13: Retrieval quality"
linktitle: "13. Retrieval quality"
summary: "Metadata filters, a NO_MATCH threshold, and a cross-encoder reranker that keeps the top 4."
weight: 140

date: "2026-10-10T00:00:00Z"
toc: true
---

Use metadata filters for service and document type. Return `NO_MATCH` when the best vector distance is above a threshold you set from the eval set. Then rerank the fused top 20 with the cross-encoder `bge-reranker-v2-m3`, served over REST, and keep the top 4.

<figure class="arch">
<script type="application/json">
{
  "title": "The full retrieval pipeline.",
  "nodes": [
    {"id": "filter", "x": 0, "y": 40, "w": 170, "label": "Metadata filters", "detail": "service, doc_type", "tone": "platform"},
    {"id": "hybrid", "x": 210, "y": 40, "w": 170, "label": "Hybrid search + RRF", "detail": "Chapter 12", "tone": "data"},
    {"id": "thr", "x": 420, "y": 40, "w": 190, "label": "Best distance ≤ threshold?", "detail": "set from the eval set", "tone": "platform"},
    {"id": "nomatch", "x": 420, "y": 180, "w": 190, "label": "NO_MATCH", "tone": "muted"},
    {"id": "rerank", "x": 650, "y": 40, "w": 190, "label": "Reranker", "detail": "bge-reranker-v2-m3 · REST", "tone": "ai"},
    {"id": "top4", "x": 650, "y": 180, "w": 190, "label": "Top 4 chunks", "detail": "to the model", "tone": "platform"},
    {"id": "log", "x": 880, "y": 40, "w": 140, "label": "Step log", "detail": "rerank duration", "tone": "muted"}
  ],
  "edges": [
    {"from": "filter", "to": "hybrid"},
    {"from": "hybrid", "to": "thr", "label": "fused top 20"},
    {"from": "thr", "to": "nomatch", "label": "no"},
    {"from": "thr", "to": "rerank", "label": "yes"},
    {"from": "rerank", "to": "top4", "label": "reorder"},
    {"from": "rerank", "to": "log", "dashed": true}
  ]
}
</script>
<figcaption>Figure 13.1. Retrieval from filter to the four chunks the model reads. The reranker adds latency, so its duration goes to the step log from Chapter 19.</figcaption>
</figure>

The reference article reports that the cross-encoder was best on all four datasets it tested (Source: VectorChord blog, 2025). Test the gain on your own eval set. The reranker adds latency, so log its duration.

PostgreSQL cannot run a neural reranker. A ColBERT rerank can run in SQL, but it needs a separate token encoder service, so this course does not use it.
