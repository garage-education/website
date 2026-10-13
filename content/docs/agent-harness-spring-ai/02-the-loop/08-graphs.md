---
title: "Chapter 8: Graphs"
linktitle: "8. Graphs"
summary: "Make the flow explicit as nodes and edges in plain Java, so every edge has a test."
weight: 90

date: "2026-10-10T00:00:00Z"
toc: true
---

A graph makes the flow explicit. Each stage is a node. Each move between stages is an edge. Keep the control flow in plain Java, so every edge has a unit test. A graph database is a different tool, used for relationships between services. Chapter 8b covers it.

<figure class="arch">
<script type="application/json">
{
  "title": "The watcher as a graph of stages.",
  "nodes": [
    {"id": "search", "x": 570, "y": 0, "w": 160, "label": "Runbook search", "detail": "hybrid + reranker", "tone": "data"},
    {"id": "window", "x": 0, "y": 120, "w": 160, "label": "Read error window", "tone": "platform"},
    {"id": "fp", "x": 190, "y": 120, "w": 160, "label": "Fingerprint", "detail": "group errors", "tone": "platform"},
    {"id": "rate", "x": 380, "y": 120, "w": 160, "label": "Rate limit", "tone": "platform"},
    {"id": "triage", "x": 570, "y": 120, "w": 160, "label": "Triage", "detail": "triage-error-group skill", "tone": "ai"},
    {"id": "lowmed", "x": 760, "y": 120, "w": 150, "label": "Low or medium", "detail": "not defined yet", "tone": "muted"},
    {"id": "empty", "x": 0, "y": 270, "w": 160, "label": "Stop", "detail": "no model call", "tone": "muted"},
    {"id": "dup", "x": 190, "y": 270, "w": 160, "label": "Suppress", "detail": "duplicate", "tone": "muted"},
    {"id": "flood", "x": 380, "y": 270, "w": 160, "label": "Stop", "detail": "flood hits the limit", "tone": "muted"},
    {"id": "approval", "x": 570, "y": 270, "w": 160, "label": "Await approval", "detail": "signal or 1-hour timer", "tone": "operator"},
    {"id": "alert", "x": 760, "y": 270, "w": 150, "label": "Post alert", "tone": "external"},
    {"id": "reject", "x": 570, "y": 400, "w": 160, "label": "Stop", "detail": "REJECTED or APPROVAL_TIMEOUT", "tone": "muted"}
  ],
  "edges": [
    {"from": "window", "to": "fp", "label": "errors"},
    {"from": "window", "to": "empty", "label": "empty"},
    {"from": "fp", "to": "rate", "label": "new"},
    {"from": "fp", "to": "dup", "label": "duplicate"},
    {"from": "rate", "to": "triage", "label": "ok"},
    {"from": "rate", "to": "flood", "label": "flood"},
    {"from": "triage", "to": "search", "label": "runbooks", "both": true},
    {"from": "triage", "to": "lowmed", "label": "low, medium"},
    {"from": "triage", "to": "approval", "label": "critical"},
    {"from": "approval", "to": "alert", "label": "approved"},
    {"from": "approval", "to": "reject", "label": "rejected, timeout"}
  ]
}
</script>
<figcaption>Figure 8.1. An illustrative watcher graph, assembled from the eval cases in Chapter 20, the triage skill in Chapter 14, and the approval in Chapter 9. Each arrow is one edge to unit-test. The course does not fix the stage order, and it does not define the low and medium path.</figcaption>
</figure>

The graph above is a teaching sketch, not the course's specification. What the watcher does with low and medium severity is <span class="needs-input">NEEDS INPUT: the low and medium severity path, for example post without approval or record only</span>.
