---
title: "Chapter 18: Context isolation"
linktitle: "18. Context isolation"
summary: "Full detail to the log, a capped fixed-shape summary to the parent."
weight: 190

date: "2026-10-10T00:00:00Z"
toc: true
---

A sub-agent keeps its full detail in the log. It returns a capped summary with a fixed shape: a finding, a confidence, and a detail id. Set the cap in code, not in the prompt. The parent's context stays small.

<figure class="arch">
<script type="application/json">
{
  "title": "Where a sub-agent's output goes.",
  "nodes": [
    {"id": "sub", "x": 0, "y": 100, "w": 190, "label": "Sub-agent", "detail": "many steps, long outputs", "tone": "platform"},
    {"id": "log", "x": 300, "y": 0, "w": 230, "label": "Log", "detail": "full detail, by detail id", "tone": "data"},
    {"id": "cap", "x": 300, "y": 190, "w": 230, "label": "Cap, in code", "detail": "finding · confidence · detail id", "tone": "platform"},
    {"id": "parent", "x": 640, "y": 190, "w": 200, "label": "Parent context", "detail": "stays small", "tone": "platform"}
  ],
  "edges": [
    {"from": "sub", "to": "log", "label": "everything"},
    {"from": "sub", "to": "cap", "label": "summary"},
    {"from": "cap", "to": "parent", "label": "capped summary"},
    {"from": "parent", "to": "log", "label": "detail id, when needed", "dashed": true}
  ]
}
</script>
<figcaption>Figure 18.1. Two outputs from one sub-agent. The detail id links the short summary back to the full record. The chapter does not say whether the parent can fetch the detail itself, so that edge is dashed.</figcaption>
</figure>
