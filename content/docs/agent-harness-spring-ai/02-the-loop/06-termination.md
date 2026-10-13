---
title: "Chapter 6: Termination"
linktitle: "6. Termination"
summary: "Every run ends for one named reason, returned in a RunResult."
weight: 70

date: "2026-10-10T00:00:00Z"
toc: true
---

A run ends in one of these ways: a final answer, a step limit, a token budget, a timeout, or loop detection. Every run returns a `RunResult` with the reason, so failures are easy to read.

<figure class="flow">
<script type="application/json">
{
  "title": "Stop checks after each model reply.",
  "steps": [
    {"label": "A model reply arrives"},
    {"label": "Does it have tool calls?", "no": "FINAL_ANSWER"},
    {"label": "Below the step limit?", "no": "STEP_LIMIT"},
    {"label": "Within the token budget?", "no": "TOKEN_BUDGET"},
    {"label": "Within the timeout?", "no": "TIMEOUT"},
    {"label": "No repeated tool call?", "no": "LOOP_DETECTED"},
    {"label": "Run the tools and continue", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 6.1. Each way a run ends maps to one <code>StopReason</code>. The chapter does not fix an order for the checks; this order is one reasonable choice. <code>APPROVAL_TIMEOUT</code> and <code>REJECTED</code> come from the approval path in Chapter 9.</figcaption>
</figure>

```java
public record RunResult(String answer, StopReason reason, int steps) {
    public enum StopReason { FINAL_ANSWER, STEP_LIMIT, TOKEN_BUDGET, TIMEOUT, LOOP_DETECTED, APPROVAL_TIMEOUT, REJECTED }
}
```
