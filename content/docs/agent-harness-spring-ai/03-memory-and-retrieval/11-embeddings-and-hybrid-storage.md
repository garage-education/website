---
title: "Chapter 11: Embeddings and hybrid storage in PostgreSQL"
linktitle: "11. Embeddings and hybrid storage"
summary: "One table holds the text, the metadata, a 1024-dimension embedding, and a keyword vector."
weight: 120

date: "2026-10-10T00:00:00Z"
toc: true
---

Use one PostgreSQL database with VectorChord for vectors, and its BM25 extension for keywords. The table holds the text, the metadata, the embedding, and the keyword vector.

```sql
CREATE TABLE IF NOT EXISTS corpus (
    id       TEXT PRIMARY KEY,
    service  TEXT NOT NULL,
    doc_type TEXT NOT NULL,
    source   TEXT NOT NULL,
    text     TEXT NOT NULL,
    emb      vector(1024),
    bm25     bm25vector
);
```

BGE-M3 runs in LM Studio and produces 1024-dimension vectors. Split documents into chunks of about 1200 characters with 150 overlapping. Embed each chunk, then insert it. A startup check confirms the vector size matches the table.

<figure class="arch">
<script type="application/json">
{
  "title": "Ingest: chunk, embed, insert.",
  "nodes": [
    {"id": "docs", "x": 0, "y": 40, "w": 150, "label": "Documents", "detail": "for example runbooks", "tone": "external"},
    {"id": "chunk", "x": 220, "y": 40, "w": 170, "label": "Chunker", "detail": "~1200 chars, 150 overlap", "tone": "platform"},
    {"id": "bge", "x": 460, "y": 40, "w": 170, "label": "BGE-M3", "detail": "in LM Studio · 1024 dims", "tone": "ai"},
    {"id": "corpus", "x": 700, "y": 40, "w": 200, "label": "corpus table", "detail": "text, metadata, emb, bm25", "tone": "data"},
    {"id": "check", "x": 700, "y": 170, "w": 200, "label": "Startup check", "detail": "vector size = vector(1024)", "tone": "muted"}
  ],
  "edges": [
    {"from": "docs", "to": "chunk", "label": "split"},
    {"from": "chunk", "to": "bge", "label": "each chunk"},
    {"from": "bge", "to": "corpus", "label": "insert"},
    {"from": "check", "to": "corpus", "label": "compares", "dashed": true}
  ]
}
</script>
<figcaption>Figure 11.1. The ingest path for one document. The figure leaves out how the <code>bm25vector</code> column is filled; see the Verify note below.</figcaption>
</figure>

<figure class="sketch">
<svg viewBox="0 0 880 150" role="img" aria-label="Three chunks of about 1200 characters, each overlapping the next by 150">
<style>.ov{fill:rgba(46,196,182,.22);stroke:none}.chunk{fill:#fff;stroke:#0d2238;stroke-width:1.5}.sk-dim{fill:#526577;font:12px "Public Sans",system-ui,sans-serif}</style>
<rect class="chunk" x="20" y="20" width="320" height="36" rx="6"/>
<rect class="chunk" x="280" y="66" width="320" height="36" rx="6"/>
<rect class="chunk" x="540" y="20" width="320" height="36" rx="6"/>
<rect class="ov" x="280" y="20" width="60" height="82"/>
<rect class="ov" x="540" y="20" width="60" height="82"/>
<text class="sk-label" x="34" y="43">chunk 1 · ~1200 chars</text>
<text class="sk-label" x="400" y="89">chunk 2 · ~1200 chars</text>
<text class="sk-label" x="620" y="43">chunk 3 · ~1200 chars</text>
<text class="sk-dim" x="282" y="125">150 shared</text>
<text class="sk-dim" x="542" y="125">150 shared</text>
</svg>
<figcaption>Figure 11.2. Overlap keeps a sentence that crosses a chunk border searchable from both sides. Not to scale.</figcaption>
</figure>

> **Verify:** Create the BM25 index with the statement in the VectorChord-BM25 repository. The reference article does not show it.
