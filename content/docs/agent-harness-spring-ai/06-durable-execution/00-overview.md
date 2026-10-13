---
title: "Part 6: Durable Execution with Temporal"
linktitle: "Part 6 overview"
summary: "Every watcher run is a Temporal workflow that survives a worker crash."
weight: 10

date: "2026-10-10T00:00:00Z"
toc: true
---

Every watcher run is a Temporal workflow. Temporal stores each step, the approval wait, and the result. A worker crash resumes the run where it stopped.

<figure class="arch">
<script type="application/json">
{
  "title": "Temporal keeps the run; workers come and go.",
  "nodes": [
    {"id": "temporal", "x": 0, "y": 60, "w": 240, "label": "Temporal server", "detail": "each step, the approval wait, the result", "tone": "operator"},
    {"id": "w1", "x": 360, "y": 0, "w": 220, "label": "Worker", "detail": "crashes after step 2", "tone": "isolated"},
    {"id": "w2", "x": 360, "y": 130, "w": 220, "label": "Worker, restarted", "detail": "resumes at step 3", "tone": "platform"}
  ],
  "edges": [
    {"from": "temporal", "to": "w1", "label": "steps 1, 2", "fromSide": "right", "toSide": "left"},
    {"from": "temporal", "to": "w2", "label": "history, then step 3", "fromSide": "right", "toSide": "left", "animated": true}
  ]
}
</script>
<figcaption>Figure 6.0. The run lives in Temporal, not in the worker. Chapter 23 turns this into an exercise.</figcaption>
</figure>
