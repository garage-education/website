---
title: "Chapter 2: Project setup"
linktitle: "2. Project setup"
summary: "A Spring Boot 4.1.1 project with the Spring AI, Session, Temporal, and OpenAI starters, pointed at LM Studio."
weight: 30

date: "2026-10-10T00:00:00Z"
toc: true
---

Create a Spring Boot 4.1.1 project with Java 17 or later. Add the Spring AI BOM 2.0.1, the Session BOM 0.6.0, the Temporal starter, and the OpenAI starter for LM Studio.

<figure class="arch">
<script type="application/json">
{
  "title": "The project and what it talks to.",
  "nodes": [
    {"id": "app", "type": "boundary", "x": 0, "y": 0, "w": 420, "h": 250, "label": "Spring Boot 4.1.1 app · Java 17+"},
    {"id": "aibom", "x": 20, "y": 40, "w": 180, "label": "Spring AI BOM", "detail": "2.0.1", "tone": "muted"},
    {"id": "sbom", "x": 220, "y": 40, "w": 180, "label": "Session BOM", "detail": "0.6.0", "tone": "muted"},
    {"id": "temporal", "x": 20, "y": 150, "w": 180, "label": "Temporal starter", "detail": "workflows and workers", "tone": "platform"},
    {"id": "openai", "x": 220, "y": 150, "w": 180, "label": "OpenAI starter", "detail": "ChatClient, embeddings", "tone": "platform"},
    {"id": "lm", "type": "boundary", "x": 490, "y": 0, "w": 260, "h": 250, "label": "LM Studio · localhost:1234"},
    {"id": "gemma", "x": 530, "y": 50, "w": 180, "label": "Gemma", "detail": "chat.options.model", "tone": "ai"},
    {"id": "bge", "x": 530, "y": 150, "w": 180, "label": "BGE-M3", "detail": "embedding.options.model", "tone": "ai"}
  ],
  "edges": [
    {"from": "openai", "to": "gemma", "label": "chat", "fromSide": "right", "toSide": "left", "animated": true},
    {"from": "openai", "to": "bge", "label": "embed", "fromSide": "right", "toSide": "left"}
  ]
}
</script>
<figcaption>Figure 2.1. The project and the local model server. The OpenAI starter reaches LM Studio through the base URL below. The figure leaves out PostgreSQL and the Temporal dev server, which later chapters connect.</figcaption>
</figure>

```properties
spring.ai.openai.base-url=http://localhost:1234
spring.ai.openai.api-key=lm-studio
spring.ai.openai.chat.options.model=YOUR-GEMMA-IDENTIFIER
spring.ai.openai.embedding.options.model=YOUR-BGE-M3-IDENTIFIER
```

Before the course, send one request with a tool definition to the Gemma model. Confirm the response contains a tool call.

<figure class="flow">
<script type="application/json">
{
  "title": "The pre-flight check.",
  "steps": [
    {"label": "Send one request with a tool definition to Gemma"},
    {"label": "Does the response contain a tool call?", "no": "Do not start the course yet"},
    {"label": "Start Chapter 3", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 2.2. The pre-flight check. Every chapter from Chapter 4 on depends on the model returning tool calls.</figcaption>
</figure>
