---
title: "Chapter 17: Agent selection"
linktitle: "17. Agent selection"
summary: "Direct, router, or supervisor. Start direct."
weight: 180

date: "2026-10-10T00:00:00Z"
toc: true
---

Three patterns exist. A direct agent handles the task itself. A router labels the task and sends it to one agent. A supervisor plans several subtasks and combines the results. Start with direct handling. Add a router only when the cost of a wrong route is clear. Test each pattern with the eval set.

<figure class="arch">
<script type="application/json">
{
  "title": "Three ways to pick who handles a task.",
  "nodes": [
    {"id": "d", "type": "boundary", "x": 0, "y": 0, "w": 230, "h": 340, "label": "Direct · start here"},
    {"id": "dt", "x": 25, "y": 50, "w": 180, "label": "Task"},
    {"id": "da", "x": 25, "y": 180, "w": 180, "label": "Agent", "detail": "handles it itself", "tone": "platform"},
    {"id": "r", "type": "boundary", "x": 260, "y": 0, "w": 270, "h": 340, "label": "Router"},
    {"id": "rt", "x": 305, "y": 50, "w": 180, "label": "Task"},
    {"id": "rr", "x": 305, "y": 140, "w": 180, "label": "Router", "detail": "labels the task", "tone": "ai"},
    {"id": "ra", "x": 280, "y": 260, "w": 110, "label": "Agent A", "tone": "platform"},
    {"id": "rb", "x": 400, "y": 260, "w": 110, "label": "Agent B", "tone": "muted"},
    {"id": "s", "type": "boundary", "x": 560, "y": 0, "w": 300, "h": 340, "label": "Supervisor"},
    {"id": "st", "x": 620, "y": 50, "w": 180, "label": "Task"},
    {"id": "ss", "x": 620, "y": 140, "w": 180, "label": "Supervisor", "detail": "plans, then combines", "tone": "ai"},
    {"id": "sa", "x": 580, "y": 260, "w": 120, "label": "Subtask 1", "tone": "platform"},
    {"id": "sb", "x": 720, "y": 260, "w": 120, "label": "Subtask 2", "tone": "platform"}
  ],
  "edges": [
    {"from": "dt", "to": "da"},
    {"from": "rt", "to": "rr"},
    {"from": "rr", "to": "ra", "label": "one route"},
    {"from": "st", "to": "ss"},
    {"from": "ss", "to": "sa", "both": true},
    {"from": "ss", "to": "sb", "both": true}
  ]
}
</script>
<figcaption>Figure 17.1. The three patterns. A router sends each task to exactly one agent; Agent B is greyed out because it was not chosen this time. A supervisor sends to several and combines the results. Each pattern is tested on the same eval set.</figcaption>
</figure>
