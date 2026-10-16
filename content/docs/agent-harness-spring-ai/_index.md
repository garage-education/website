---
title: Building an Agent Harness with Spring AI
linktitle: Agent Harness with Spring AI
summary: Build the code around a large language model in Java. Tools, the agent loop, memory, hybrid retrieval, skills, sub-agents, evals, and durable execution with Temporal, one chapter at a time.
weight: 1

date: "2026-10-10T00:00:00Z"
lastmod: "2026-10-16T00:00:00Z"
draft: false
toc: true
---

## About "Building an Agent Harness with Spring AI"

This book teaches Java engineers to build an agent harness with Spring AI. The running example is the Log Incident Watcher. Read the chapters in order. Each chapter adds one idea. Run the code in each chapter before you read the next one. All examples use fake data and run offline.

## What you will build

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

## Course Content

1. [Start here]({{< relref "/docs/agent-harness-spring-ai/00-start" >}})
    1. [Front matter]({{< relref "/docs/agent-harness-spring-ai/00-start/01-front-matter" >}})
    1. [Glossary]({{< relref "/docs/agent-harness-spring-ai/00-start/02-glossary" >}})
1. [Part 1: Foundations]({{< relref "/docs/agent-harness-spring-ai/01-foundations" >}})
    1. [Chapter 1: Why a harness?]({{< relref "/docs/agent-harness-spring-ai/01-foundations/01-why-a-harness" >}})
    1. [Chapter 2: Project setup]({{< relref "/docs/agent-harness-spring-ai/01-foundations/02-project-setup" >}})
    1. [Chapter 3: The model call]({{< relref "/docs/agent-harness-spring-ai/01-foundations/03-the-model-call" >}})
    1. [Chapter 4: Tools]({{< relref "/docs/agent-harness-spring-ai/01-foundations/04-tools" >}})
1. [Part 2: The Loop]({{< relref "/docs/agent-harness-spring-ai/02-the-loop" >}})
    1. [Chapter 5: Writing the agent loop by hand]({{< relref "/docs/agent-harness-spring-ai/02-the-loop/05-writing-the-agent-loop-by-hand" >}})
    1. [Chapter 6: Termination]({{< relref "/docs/agent-harness-spring-ai/02-the-loop/06-termination" >}})
    1. [Chapter 7: Guardrails]({{< relref "/docs/agent-harness-spring-ai/02-the-loop/07-guardrails" >}})
    1. [Chapter 8: Graphs]({{< relref "/docs/agent-harness-spring-ai/02-the-loop/08-graphs" >}})
    1. [Chapter 9: Human-in-the-loop]({{< relref "/docs/agent-harness-spring-ai/02-the-loop/09-human-in-the-loop" >}})
1. [Part 3: Memory and Retrieval]({{< relref "/docs/agent-harness-spring-ai/03-memory-and-retrieval" >}})
    1. [Chapter 10: Short-term memory with Spring AI Session]({{< relref "/docs/agent-harness-spring-ai/03-memory-and-retrieval/10-short-term-memory-with-spring-ai-session" >}})
    1. [Chapter 11: Embeddings and hybrid storage in PostgreSQL]({{< relref "/docs/agent-harness-spring-ai/03-memory-and-retrieval/11-embeddings-and-hybrid-storage" >}})
    1. [Chapter 12: Hybrid retrieval inside the loop]({{< relref "/docs/agent-harness-spring-ai/03-memory-and-retrieval/12-hybrid-retrieval-inside-the-loop" >}})
    1. [Chapter 13: Retrieval quality]({{< relref "/docs/agent-harness-spring-ai/03-memory-and-retrieval/13-retrieval-quality" >}})
1. [Part 4: Skills and Agents]({{< relref "/docs/agent-harness-spring-ai/04-skills-and-agents" >}})
    1. [Chapter 14: Skills as files]({{< relref "/docs/agent-harness-spring-ai/04-skills-and-agents/14-skills-as-files" >}})
    1. [Chapter 15: Skill selection]({{< relref "/docs/agent-harness-spring-ai/04-skills-and-agents/15-skill-selection" >}})
    1. [Chapter 16: Sub-agents]({{< relref "/docs/agent-harness-spring-ai/04-skills-and-agents/16-sub-agents" >}})
    1. [Chapter 17: Agent selection]({{< relref "/docs/agent-harness-spring-ai/04-skills-and-agents/17-agent-selection" >}})
    1. [Chapter 18: Context isolation]({{< relref "/docs/agent-harness-spring-ai/04-skills-and-agents/18-context-isolation" >}})
1. [Part 5: Observability, Evaluation, and Cost]({{< relref "/docs/agent-harness-spring-ai/05-observability-evaluation-cost" >}})
    1. [Chapter 19: Step logging]({{< relref "/docs/agent-harness-spring-ai/05-observability-evaluation-cost/19-step-logging" >}})
    1. [Chapter 20: A small eval set]({{< relref "/docs/agent-harness-spring-ai/05-observability-evaluation-cost/20-a-small-eval-set" >}})
    1. [Chapter 21: Failure drills]({{< relref "/docs/agent-harness-spring-ai/05-observability-evaluation-cost/21-failure-drills" >}})
    1. [Chapter 22: Cost optimization]({{< relref "/docs/agent-harness-spring-ai/05-observability-evaluation-cost/22-cost-optimization" >}})
1. [Part 6: Durable Execution with Temporal]({{< relref "/docs/agent-harness-spring-ai/06-durable-execution" >}})
    1. [Part 6: Durable Execution with Temporal]({{< relref "/docs/agent-harness-spring-ai/06-durable-execution/00-overview" >}})
    1. [Chapter 23: Run state and messages]({{< relref "/docs/agent-harness-spring-ai/06-durable-execution/23-run-state-and-messages" >}})
    1. [Chapter 24: Temporal basics for the watcher]({{< relref "/docs/agent-harness-spring-ai/06-durable-execution/24-temporal-basics-for-the-watcher" >}})
1. [Part 7: Capstone]({{< relref "/docs/agent-harness-spring-ai/07-capstone" >}})
    1. [Chapter 25: Assemble the Log Incident Watcher]({{< relref "/docs/agent-harness-spring-ai/07-capstone/25-assemble-the-log-incident-watcher" >}})
1. [About this course]({{< relref "/docs/agent-harness-spring-ai/99-about" >}})
    1. [Progress, open items, and changelog]({{< relref "/docs/agent-harness-spring-ai/99-about/01-progress-and-changelog" >}})
