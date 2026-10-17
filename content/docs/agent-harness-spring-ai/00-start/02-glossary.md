---
title: "Glossary"
linktitle: "Glossary"
summary: "Every term the course uses, defined once."
weight: 30

date: "2026-10-10T00:00:00Z"
toc: true
---

<figure class="arch">
<script type="application/json">
{
  "title": "How the core terms fit together.",
  "nodes": [
    {"id": "agent", "type": "boundary", "x": 0, "y": 0, "w": 860, "h": 330, "label": "Agent = model + harness + goal"},
    {"id": "goal", "x": 30, "y": 50, "w": 170, "label": "Goal", "detail": "what the run must achieve"},
    {"id": "harness", "type": "boundary", "x": 230, "y": 40, "w": 400, "h": 270, "label": "Harness"},
    {"id": "loop", "x": 250, "y": 80, "w": 170, "label": "Loop", "detail": "model call, tools, result", "tone": "platform"},
    {"id": "term", "x": 440, "y": 80, "w": 170, "label": "Termination", "detail": "the rule that ends a run", "tone": "platform"},
    {"id": "tools", "x": 250, "y": 170, "w": 170, "label": "Tools", "detail": "Java methods", "tone": "platform"},
    {"id": "skills", "x": 440, "y": 170, "w": 170, "label": "Skills", "detail": "loaded only when needed", "tone": "platform"},
    {"id": "memory", "x": 250, "y": 245, "w": 360, "label": "Memory", "detail": "short-term conversation, long-term store", "tone": "data"},
    {"id": "model", "x": 660, "y": 80, "w": 170, "label": "Model", "detail": "text in, text out", "tone": "ai"},
    {"id": "window", "x": 660, "y": 200, "w": 170, "label": "Context window", "detail": "measured in tokens", "tone": "muted"}
  ],
  "edges": [
    {"from": "goal", "to": "loop", "label": "drives"},
    {"from": "loop", "to": "model", "label": "prompt / reply", "fromSide": "top", "toSide": "top", "both": true, "animated": true},
    {"from": "model", "to": "window", "label": "reads one"}
  ]
}
</script>
<figcaption>Figure 0.2. How the core terms fit together. Retrieval, evaluation, and durable-execution terms are left out; each has its own part of the course.</figcaption>
</figure>

- **Model.** A large language model. It takes text in and returns text out.
- **Harness.** The code around a model. It sends requests, runs tools, keeps state, and decides when to stop.
- **Agent.** A model plus a harness plus a goal.
- **Tool.** A Java method the model can ask the harness to run.
- **Tool call.** The model's request to run a tool. It names the tool and gives arguments.
- **Advisor.** A Spring AI class that runs around each model call. It can change the request or the reply. Tool calling, memory, and retrieval are each one advisor.
- **Loop.** The cycle of model call, tool execution, and result. It ends when the run stops.
- **Termination.** The rule that ends a run.
- **Context window.** The text the model can read in one call. It is measured in tokens.
- **Token.** A small piece of text. Providers bill by token.
- **Skill.** A file of instructions for one task. The harness loads it only when needed.
- **Sub-agent.** An agent that a parent agent calls as a tool.
- **Memory.** Information kept across model calls. Short-term memory is the recent conversation. Long-term memory is stored outside it.
- **Embedding.** A list of numbers that represents the meaning of a text.
- **Vector store.** A database that finds texts with similar embeddings.
- **BM25.** A keyword scoring method. It rewards rare words that appear often in a document.
- **Hybrid search.** Keyword search and vector search, merged into one result list.
- **RRF (Reciprocal Rank Fusion).** A way to merge ranked lists by rank position, not by score.
- **Reranker.** A model that scores a query and each candidate together, then reorders the candidates.
- **RAG (retrieval-augmented generation).** The harness fetches relevant documents before the model answers.
- **HITL (human-in-the-loop).** A run that pauses until a person approves an action.
- **Graph.** A flow of nodes and edges. A knowledge graph stores relationships between things.
- **Durable execution.** A run that survives crashes and restarts because its state is stored.
- **Workflow (Temporal).** The durable definition of one run.
- **Activity (Temporal).** A unit of work with side effects, such as a model call. Temporal retries it.
- **Signal (Temporal).** A message sent to a running workflow, such as an approval.
- **Eval.** A fixed set of test inputs with expected properties. Run it before each change.
- **Prompt caching.** The provider reuses work for a stable part of the prompt. It lowers cost.
