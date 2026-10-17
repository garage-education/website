---
title: "Front matter"
linktitle: "Front matter"
summary: "What the course teaches, the pinned versions, and the local services every chapter runs against."
weight: 20

date: "2026-10-10T00:00:00Z"
toc: true
---

Oct 10, 2026 · @Ahmed Hassanien

This book teaches engineers to build an agent harness with Spring AI in Java. Chapters 2 to 6 also show every step in Python with LangChain. The running example is the Log Incident Watcher. Read the chapters in order. Each chapter adds one idea. Run the code in each chapter before you read the next one. All examples use fake data and run offline.

**Versions:** Spring Boot 4.1.1, Spring AI 2.0.1, Spring AI Session 0.6.0, Temporal 1.35.0. Use released versions only.

**Local services:** PostgreSQL 17 with VectorChord, BM25, and AGE. LM Studio with Gemma for chat and BGE-M3 for embeddings. A reranker container for bge-reranker-v2-m3. A Temporal dev server.

<figure class="arch">
<script type="application/json">
{
  "title": "The local stack every chapter runs against.",
  "nodes": [
    {"id": "lm", "type": "boundary", "x": 300, "y": 0, "w": 520, "h": 120, "label": "LM Studio"},
    {"id": "app", "x": 0, "y": 175, "w": 200, "label": "Spring Boot app", "detail": "the harness you build", "tone": "platform"},
    {"id": "gemma", "x": 320, "y": 40, "w": 230, "label": "Gemma", "detail": "chat model", "tone": "ai"},
    {"id": "bge", "x": 570, "y": 40, "w": 230, "label": "BGE-M3", "detail": "embeddings", "tone": "ai"},
    {"id": "rerank", "x": 320, "y": 160, "w": 230, "label": "Reranker container", "detail": "bge-reranker-v2-m3", "tone": "ai"},
    {"id": "pg", "x": 320, "y": 260, "w": 230, "label": "PostgreSQL 17", "detail": "VectorChord, BM25, AGE", "tone": "data"},
    {"id": "temporal", "x": 570, "y": 260, "w": 230, "label": "Temporal dev server", "detail": "durable runs", "tone": "operator"}
  ],
  "edges": [
    {"from": "app", "to": "gemma", "label": "chat", "fromSide": "top", "toSide": "left", "animated": true},
    {"from": "app", "to": "rerank", "label": "rerank", "fromSide": "right", "toSide": "left"},
    {"from": "app", "to": "pg", "label": "read / write", "fromSide": "bottom", "toSide": "left", "both": true}
  ]
}
</script>
<figcaption>Figure 0.1. The local stack. Everything runs on one machine with fake data. The figure leaves out the embedding and Temporal connections from the app; later chapters draw each one where it is used.</figcaption>
</figure>

## How to use this course

The code lives in the `garage-education/harness-engineering` repository on GitHub. Clone it before Chapter 2:

```bash
git clone git@github.com:garage-education/harness-engineering.git
```

Pick a language: Java with Spring AI, or Python with LangChain. From Chapter 2 to Chapter 6, every code sample has a **Java** tab and a **Python** tab. Your choice applies to every page and is remembered.

You need LM Studio, plus JDK 27 for Java or uv for Python. Chapter 2 sets up the rest.

Work through each chapter in four steps:

1. **Read** the chapter. It shows the code for that chapter only.
2. **Write** the code, or compare it with `java/src/main/java/com/garageeducation/harness/` or `python/src/harness/` in the repository.
3. **Send** the chapter's requests in `requests/harness.http`. Open the file in IntelliJ IDEA, or in VS Code with the REST Client extension.
4. **Read** the console log. Each chapter shows the log lines to expect. Chapter 2, Table 2.1 explains every log tag.

The repository's `java/` and `python/` folders hold the code after Chapter 6. Both apps listen on port 8080 and answer the same requests. Run one at a time. It is ahead of Chapters 3 to 5. Follow the code in each chapter, not the final files.

Model replies differ between runs. Compare the shape of each reply and log, not the exact words.
