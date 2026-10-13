---
title: "Chapter 23: Run state and messages"
linktitle: "23. Run state and messages"
summary: "Temporal holds the run state, Session holds the messages, and the workflow id joins them."
weight: 240

date: "2026-10-10T00:00:00Z"
toc: true
---

Temporal workflow history holds the run state. It holds the step count, the state, the approval, and the result. Spring AI Session holds the messages and tool calls. Use the workflow id as the session id. Do not store run state in a separate table. Two stores for one run drift apart.

<figure class="arch">
<script type="application/json">
{
  "title": "One run, two stores, one id.",
  "nodes": [
    {"id": "id", "x": 300, "y": 0, "w": 220, "label": "Workflow id", "detail": "= session id", "tone": "platform"},
    {"id": "hist", "x": 0, "y": 140, "w": 260, "label": "Temporal workflow history", "detail": "step count, state, approval, result", "tone": "operator"},
    {"id": "sess", "x": 560, "y": 140, "w": 260, "label": "Spring AI Session", "detail": "messages and tool calls", "tone": "data"},
    {"id": "table", "x": 300, "y": 270, "w": 220, "label": "Separate run-state table", "detail": "do not add: it drifts", "tone": "isolated"}
  ],
  "edges": [
    {"from": "id", "to": "hist", "label": "run state"},
    {"from": "id", "to": "sess", "label": "messages"}
  ]
}
</script>
<figcaption>Figure 23.1. Each fact about a run has exactly one home. A third store, struck out here, would have to agree with the other two and eventually would not.</figcaption>
</figure>

**Exercise.** Start a run. Kill the worker after step 2. Restart it. Confirm the run completes without repeating step 1.

<figure class="seq">
<script type="application/json">
{
  "title": "The exercise: kill, restart, resume.",
  "lifelines": [
    {"id": "you", "label": "You", "tone": "external"},
    {"id": "temporal", "label": "Temporal", "tone": "operator"},
    {"id": "w1", "label": "Worker", "tone": "platform"},
    {"id": "w2", "label": "Worker, restarted", "tone": "platform"}
  ],
  "messages": [
    {"from": "you", "to": "temporal", "label": "start a run"},
    {"from": "temporal", "to": "w1", "label": "run step 1"},
    {"from": "w1", "to": "temporal", "label": "step 1 done, recorded", "kind": "response"},
    {"from": "temporal", "to": "w1", "label": "run step 2"},
    {"from": "w1", "to": "temporal", "label": "step 2 done, recorded", "kind": "response"},
    {"from": "you", "to": "w1", "label": "kill the worker", "kind": "note"},
    {"from": "temporal", "to": "w2", "label": "history: steps 1 and 2 already done"},
    {"from": "w2", "to": "temporal", "label": "steps 3 onward; step 1 is not repeated", "kind": "response"},
    {"from": "temporal", "to": "you", "label": "run completes", "kind": "response"}
  ]
}
</script>
<figcaption>Figure 23.2. What you should see in the exercise. Recorded results are replayed from history, not run again.</figcaption>
</figure>
