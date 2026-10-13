---
title: "Chapter 16: Sub-agents"
linktitle: "16. Sub-agents"
summary: "A focused agent with its own prompt, allowlist, and step limit, called as a tool."
weight: 170

date: "2026-10-10T00:00:00Z"
toc: true
---

A sub-agent has its own system prompt, its own tool allowlist, and its own step limit. The parent calls it through a tool that returns a short summary. A focused agent does one job well.

<figure class="arch">
<script type="application/json">
{
  "title": "A parent calls a sub-agent through a tool.",
  "nodes": [
    {"id": "pb", "type": "boundary", "x": 0, "y": 0, "w": 300, "h": 240, "label": "Parent agent"},
    {"id": "parent", "x": 30, "y": 50, "w": 240, "label": "Parent loop", "detail": "its own goal", "tone": "platform"},
    {"id": "tool", "x": 30, "y": 150, "w": 240, "label": "Sub-agent tool", "detail": "one entry in the parent's allowlist", "tone": "platform"},
    {"id": "sb", "type": "boundary", "x": 370, "y": 0, "w": 450, "h": 240, "label": "Sub-agent"},
    {"id": "sloop", "x": 400, "y": 50, "w": 190, "label": "Sub-agent loop", "tone": "platform"},
    {"id": "prompt", "x": 610, "y": 40, "w": 190, "label": "Own system prompt", "tone": "muted"},
    {"id": "allow", "x": 610, "y": 105, "w": 190, "label": "Own tool allowlist", "tone": "muted"},
    {"id": "limit", "x": 610, "y": 170, "w": 190, "label": "Own step limit", "tone": "muted"}
  ],
  "edges": [
    {"from": "parent", "to": "tool", "label": "tool call"},
    {"from": "tool", "to": "sloop", "label": "task", "fromSide": "right", "toSide": "bottom"},
    {"from": "sloop", "to": "parent", "label": "short summary", "fromSide": "left", "toSide": "right"}
  ]
}
</script>
<figcaption>Figure 16.1. To the parent, a sub-agent is one more tool. Its prompt, tools, and step limit are its own. Chapter 18 fixes the shape of the summary.</figcaption>
</figure>
