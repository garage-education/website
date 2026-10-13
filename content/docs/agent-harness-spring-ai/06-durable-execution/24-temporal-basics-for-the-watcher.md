---
title: "Chapter 24: Temporal basics for the watcher"
linktitle: "24. Temporal basics"
summary: "Workflow, activity, signal, timer, retry policy, and query, and the determinism rule."
weight: 250

date: "2026-10-10T00:00:00Z"
toc: true
---

| Concept | Use in the watcher |
| --- | --- |
| Workflow | One watcher run |
| Activity | One model call, one tool call, one alert post |
| Signal | Human approval |
| Timer | Approval deadline |
| Retry policy | Retry a failed model or tool call |
| Query | Read the current state |

**Determinism rule.** Workflow code must give the same result on replay. Model calls, tool calls, database writes, and REST calls go in activities. Use `Workflow.await`, `Workflow.sleep`, and `Workflow.currentTimeMillis()` in the workflow. Do not use `Thread.sleep` or `Instant.now()` there.

<figure class="flow">
<script type="application/json">
{
  "title": "Where does this line of code go?",
  "steps": [
    {"label": "Is it pure logic: same input, same result on replay?", "no": "Activity: model, tool, database, or REST call"},
    {"label": "Does it wait or read the time?", "no": "Workflow code, as is"},
    {"label": "Workflow code, using Workflow.await, Workflow.sleep, or Workflow.currentTimeMillis()", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 24.1. The determinism rule as two questions. <code>Thread.sleep</code> and <code>Instant.now()</code> never appear in workflow code.</figcaption>
</figure>

```java
@WorkflowInterface
public interface WatcherWorkflow {
    @WorkflowMethod RunResult run(WatchRequest request);
    @SignalMethod void decideApproval(boolean approved);
    @QueryMethod String state();
}
```

<figure class="seq">
<script type="application/json">
{
  "title": "WatcherWorkflow: start, activities, query, signal, and result.",
  "lifelines": [
    {"id": "rest", "label": "REST endpoint", "tone": "platform"},
    {"id": "wf", "label": "WatcherWorkflow", "tone": "operator"},
    {"id": "act", "label": "Activities", "tone": "platform"},
    {"id": "person", "label": "Person", "tone": "external"}
  ],
  "messages": [
    {"from": "rest", "to": "wf", "label": "start: run(WatchRequest)"},
    {"from": "wf", "to": "act", "label": "model call (retry policy)"},
    {"from": "act", "to": "wf", "label": "reply", "kind": "response"},
    {"from": "wf", "to": "act", "label": "tool call (retry policy)"},
    {"from": "act", "to": "wf", "label": "result", "kind": "response"},
    {"from": "wf", "to": "wf", "label": "critical: timer for the approval deadline"},
    {"from": "rest", "to": "wf", "label": "query: state()"},
    {"from": "wf", "to": "rest", "label": "current state", "kind": "response"},
    {"from": "person", "to": "wf", "label": "signal: decideApproval(true)"},
    {"from": "wf", "to": "act", "label": "alert post"},
    {"from": "wf", "to": "rest", "label": "RunResult", "kind": "response"}
  ]
}
</script>
<figcaption>Figure 24.2. Every concept in the table, in one run. The figure leaves out how the person's approval reaches the signal; in the exercise below, a REST call sends it.</figcaption>
</figure>

> **Verify:** Confirm the annotation packages and the starter configuration keys for SDK 1.35.0. Temporal's Spring Boot starter starts the worker automatically when the app starts.

**Exercise.** Start a run through a REST endpoint. Read its state with a query. Approve a critical run. Confirm one alert posts.
