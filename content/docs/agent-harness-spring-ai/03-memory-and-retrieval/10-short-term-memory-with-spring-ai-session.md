---
title: "Chapter 10: Short-term memory with Spring AI Session"
linktitle: "10. Short-term memory"
summary: "Session keeps every message and tool call in PostgreSQL. The window sent to the model is a separate choice."
weight: 110

date: "2026-10-10T00:00:00Z"
toc: true
---

Spring AI Session stores every message and tool call in PostgreSQL. Spring AI's JDBC chat memory drops tool call messages, so this course does not use it. The workflow id is the session id.

```java
sessions.appendMessage(sessionId, new UserMessage(question));
List<Message> history = sessions.getMessages(sessionId);
```

<figure class="arch">
<script type="application/json">
{
  "title": "Full history in the database, a chosen window to the model.",
  "nodes": [
    {"id": "pgb", "type": "boundary", "x": 260, "y": 0, "w": 260, "h": 260, "label": "PostgreSQL"},
    {"id": "harness", "x": 0, "y": 40, "w": 200, "label": "Harness", "detail": "session id = workflow id", "tone": "platform"},
    {"id": "session", "x": 280, "y": 40, "w": 220, "label": "Spring AI Session", "detail": "every message and tool call", "tone": "data"},
    {"id": "jdbc", "x": 280, "y": 170, "w": 220, "label": "JDBC chat memory", "detail": "drops tool calls · not used", "tone": "isolated"},
    {"id": "window", "x": 580, "y": 40, "w": 190, "label": "Context window", "detail": "a separate choice", "tone": "platform"},
    {"id": "model", "x": 580, "y": 170, "w": 190, "label": "Model", "tone": "ai"}
  ],
  "edges": [
    {"from": "harness", "to": "session", "label": "appendMessage"},
    {"from": "session", "to": "window", "label": "getMessages"},
    {"from": "window", "to": "model", "label": "prompt", "animated": true}
  ]
}
</script>
<figcaption>Figure 10.1. The database keeps everything. The harness decides how much of it to send. The figure leaves out how the window is chosen; the chapter leaves that open.</figcaption>
</figure>

The full history stays in the database. The window sent to the model is a separate choice. Verify the bean name and the `create` signature in the Session README.
