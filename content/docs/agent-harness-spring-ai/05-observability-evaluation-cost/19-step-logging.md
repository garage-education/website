---
title: "Chapter 19: Step logging"
linktitle: "19. Step logging"
summary: "One JSON line per model call and per tool call, searchable by run id."
weight: 200

date: "2026-10-10T00:00:00Z"
toc: true
---

Write one JSON line per model call and per tool call. Each line holds the run id, step number, kind, tool name, arguments, token counts, duration, and stop reason. A failure is easy to find when you search by run id.

<figure class="arch">
<script type="application/json">
{
  "title": "Every call in the loop leaves one line.",
  "nodes": [
    {"id": "loop", "type": "boundary", "x": 0, "y": 0, "w": 420, "h": 150, "label": "One run · run id"},
    {"id": "m", "x": 20, "y": 50, "w": 180, "label": "Model call", "detail": "step n", "tone": "ai"},
    {"id": "t", "x": 220, "y": 50, "w": 180, "label": "Tool call", "detail": "step n", "tone": "platform"},
    {"id": "log", "x": 500, "y": 50, "w": 200, "label": "Step log", "detail": "one JSON line per call", "tone": "data"},
    {"id": "you", "x": 760, "y": 50, "w": 120, "label": "You", "detail": "search by run id", "tone": "external"}
  ],
  "edges": [
    {"from": "m", "to": "log", "fromSide": "bottom", "toSide": "bottom"},
    {"from": "t", "to": "log", "label": "one line each"},
    {"from": "you", "to": "log", "label": "search"}
  ]
}
</script>
<figcaption>Figure 19.1. Both kinds of call write to the same log. Because every line carries the run id, one search returns the whole run in step order.</figcaption>
</figure>

An illustrative pair of lines, one per kind. The field names are an example; the chapter fixes the content, not the spelling.

```json
{"runId":"run-42","step":1,"kind":"model","tool":null,"args":null,"tokensIn":812,"tokensOut":41,"durationMs":930,"stopReason":null}
{"runId":"run-42","step":1,"kind":"tool","tool":"countErrors","args":{"service":"checkout","minutes":15},"tokensIn":0,"tokensOut":0,"durationMs":4,"stopReason":null}
```
