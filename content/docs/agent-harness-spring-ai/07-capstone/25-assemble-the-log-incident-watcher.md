---
title: "Chapter 25: Assemble the Log Incident Watcher"
linktitle: "25. Assemble the watcher"
summary: "Every part together, with each model and tool call as a Temporal activity."
weight: 260

date: "2026-10-10T00:00:00Z"
toc: true
---

The capstone runs every part together. Each run is a Temporal workflow. Each model call and each tool call is an activity. Approval is a signal. Memory is Spring AI Session. Retrieval is hybrid search with a cross-encoder reranker.

<figure class="arch">
<script type="application/json">
{
  "title": "The Log Incident Watcher, assembled.",
  "nodes": [
    {"id": "worker", "type": "boundary", "x": 0, "y": 110, "w": 880, "h": 270, "label": "Spring Boot app · worker \"watcher\""},
    {"id": "person", "x": 0, "y": 0, "w": 160, "label": "Person", "detail": "starts runs, approves", "tone": "external"},
    {"id": "rest", "x": 200, "y": 0, "w": 160, "label": "REST endpoint", "detail": "start, query, approve", "tone": "platform"},
    {"id": "temporal", "x": 400, "y": 0, "w": 220, "label": "Temporal server", "detail": "history, timers, signals", "tone": "operator"},
    {"id": "wf", "x": 400, "y": 150, "w": 220, "label": "WatcherWorkflowImpl", "detail": "the loop, stop rules, approval wait", "tone": "operator"},
    {"id": "tool", "x": 80, "y": 280, "w": 180, "label": "ToolActivity", "detail": "allowlist, run, save result", "tone": "platform"},
    {"id": "model", "x": 420, "y": 280, "w": 180, "label": "ModelActivity", "detail": "read session, call, save last", "tone": "platform"},
    {"id": "alert", "x": 680, "y": 280, "w": 180, "label": "AlertActivity", "detail": "only after approval", "tone": "platform"},
    {"id": "rerank", "x": 0, "y": 440, "w": 160, "label": "Reranker", "detail": "bge-reranker-v2-m3", "tone": "ai"},
    {"id": "pg", "x": 210, "y": 440, "w": 200, "label": "PostgreSQL", "detail": "Session, corpus, audit", "tone": "data"},
    {"id": "gemma", "x": 420, "y": 440, "w": 180, "label": "Gemma", "detail": "LM Studio", "tone": "ai"},
    {"id": "channel", "x": 680, "y": 440, "w": 180, "label": "Alert channel", "tone": "external"}
  ],
  "edges": [
    {"from": "person", "to": "rest"},
    {"from": "rest", "to": "temporal"},
    {"from": "temporal", "to": "wf", "label": "workflow tasks", "both": true},
    {"from": "wf", "to": "tool", "fromSide": "left", "toSide": "top"},
    {"from": "wf", "to": "model", "label": "activities"},
    {"from": "wf", "to": "alert", "fromSide": "right", "toSide": "top"},
    {"from": "tool", "to": "rerank", "fromSide": "bottom", "toSide": "top"},
    {"from": "tool", "to": "pg", "fromSide": "bottom", "toSide": "top"},
    {"from": "model", "to": "pg", "fromSide": "left", "toSide": "top"},
    {"from": "model", "to": "gemma", "label": "chat", "animated": true},
    {"from": "alert", "to": "channel"}
  ]
}
</script>
<figcaption>Figure 25.1. Every part of the course in one picture. The workflow only schedules; the three activities do all the I/O. The figure leaves out the step log from Chapter 19 and the triage cache from Chapter 22.</figcaption>
</figure>

Temporal's Spring AI integration does not yet support Spring AI 2.x. The integration is in public preview with Spring AI 1.1.0 listed. Upgrading it is tracked in temporalio/ai-integrations PR #40. This chapter uses plain activities that do the same job.

| Activity | Role |
| --- | --- |
| `ModelActivity` | Reads the session, calls the model, saves the reply last |
| `ToolActivity` | Checks the allowlist, runs the tool, saves the result |
| `AlertActivity` | Posts the alert, only after approval |

The workflow runs the loop. It stops on a final answer, a `submitFinding` tool call, the step limit, loop detection, an approval timeout, or a rejection. It never calls a model or a tool itself.

| Stop rule | Limit | `StopReason` |
| --- | --- | --- |
| Final answer | — | `FINAL_ANSWER` |
| `submitFinding` tool call | — | <span class="needs-input">NEEDS INPUT: which StopReason a submitFinding stop returns; the enum has no dedicated value</span> |
| Step limit | `MAX_STEPS = 12` | `STEP_LIMIT` |
| Loop detection | `MAX_REPEATS = 3` | `LOOP_DETECTED` |
| Approval timeout | one hour (Chapter 9) | `APPROVAL_TIMEOUT` |
| Rejection | — | `REJECTED` |

<p class="caption"><strong>Table 25.1.</strong> The capstone's stop rules mapped to the <code>StopReason</code> enum from Chapter 6.</p>

```java
@WorkflowImpl(workers = "watcher")
public class WatcherWorkflowImpl implements WatcherWorkflow {
    private static final int MAX_STEPS = 12;
    private static final int MAX_REPEATS = 3;
    // activity stubs for model, tools, and alerts
    // loop: model turn, then each tool call, then stop rules
}
```

<figure class="seq">
<script type="application/json">
{
  "title": "One critical run, end to end.",
  "lifelines": [
    {"id": "rest", "label": "REST endpoint", "tone": "platform"},
    {"id": "wf", "label": "WatcherWorkflowImpl", "tone": "operator"},
    {"id": "model", "label": "ModelActivity", "tone": "platform"},
    {"id": "tool", "label": "ToolActivity", "tone": "platform"},
    {"id": "alert", "label": "AlertActivity", "tone": "platform"},
    {"id": "person", "label": "Person", "tone": "external"}
  ],
  "messages": [
    {"from": "rest", "to": "wf", "label": "start run(WatchRequest)"},
    {"from": "wf", "to": "model", "label": "model turn"},
    {"from": "model", "to": "model", "label": "read session, call Gemma, save reply last"},
    {"from": "model", "to": "wf", "label": "reply with tool calls", "kind": "response"},
    {"from": "wf", "to": "tool", "label": "each tool call"},
    {"from": "tool", "to": "tool", "label": "check allowlist, run tool, save result"},
    {"from": "tool", "to": "wf", "label": "results", "kind": "response"},
    {"from": "wf", "to": "wf", "label": "check stop rules: steps ≤ 12, repeats < 3"},
    {"from": "wf", "to": "tool", "label": "Repeat model turns until the model calls submitFinding", "kind": "note"},
    {"from": "wf", "to": "wf", "label": "finding is critical: wait for approval"},
    {"from": "person", "to": "wf", "label": "signal: decideApproval(true)"},
    {"from": "wf", "to": "alert", "label": "post the alert"},
    {"from": "alert", "to": "wf", "label": "posted", "kind": "response"},
    {"from": "wf", "to": "rest", "label": "RunResult", "kind": "response"}
  ]
}
</script>
<figcaption>Figure 25.2. A critical run, end to end. Step through it with Previous and Next. Placing the approval after <code>submitFinding</code> combines this chapter with Chapter 9.</figcaption>
</figure>

**Rule to teach.** A retried activity can save its message twice if it fails after saving. Save last. Verify whether Session accepts a message id for idempotent saves.

**Switching later.** When `io.temporal:spring-ai` ships a public release, replace the model activity with its chat model class. The stop rules and approval code stay the same.

**Final exercise.** Run the full eval set. Break one drill from Chapter 21, fix it, and record the final score.
