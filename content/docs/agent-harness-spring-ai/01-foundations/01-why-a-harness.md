---
title: "Chapter 1: Why a harness?"
linktitle: "1. Why a harness?"
summary: "A model only reads and writes text. The harness adds five jobs around it."
weight: 20

date: "2026-10-10T00:00:00Z"
toc: true
---

A model reads text and writes text. It cannot run code, read files, or remember past calls. The harness adds those abilities. It does five jobs. It sends the prompt. It reads the reply. It runs the tools the model asks for. It returns the tool results. It decides when the run stops.

<figure class="seq">
<script type="application/json">
{
  "title": "One harness run: the five jobs, in order.",
  "lifelines": [
    {"id": "you", "label": "Engineer", "tone": "external"},
    {"id": "harness", "label": "Harness", "tone": "platform"},
    {"id": "model", "label": "Model", "tone": "subscriber"},
    {"id": "tool", "label": "countErrors tool", "tone": "platform"}
  ],
  "messages": [
    {"from": "you", "to": "harness", "label": "Is checkout slow?"},
    {"from": "harness", "to": "model", "label": "Job 1: send the prompt and the tool list"},
    {"from": "model", "to": "harness", "label": "tool call: countErrors(checkout)", "kind": "response"},
    {"from": "harness", "to": "harness", "label": "Job 2: read the reply"},
    {"from": "harness", "to": "tool", "label": "Job 3: run the tool"},
    {"from": "tool", "to": "harness", "label": "412 errors", "kind": "response"},
    {"from": "harness", "to": "model", "label": "Job 4: return the tool result"},
    {"from": "model", "to": "harness", "label": "answer, based on the real count", "kind": "response"},
    {"from": "harness", "to": "harness", "label": "Job 5: no more tool calls, so stop"},
    {"from": "harness", "to": "you", "label": "answer", "kind": "response"}
  ]
}
</script>
<figcaption>Figure 1.1. One harness run, with each of the five jobs labelled. Use Previous and Next to step through it. The count of 412 is the fake data from Chapter 4.</figcaption>
</figure>

**Example.** Asked alone, a model can only guess whether checkout is slow. With a harness, the model calls a `countErrors` tool, reads the real count, and answers from that data.

**Objectives:** describe a model call, name the five harness jobs, and explain what the course builds.
