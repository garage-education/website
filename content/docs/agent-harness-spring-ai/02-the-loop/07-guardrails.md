---
title: "Chapter 7: Guardrails"
linktitle: "7. Guardrails"
summary: "Argument checks, an allowlist, and loop detection, enforced in code."
weight: 80

date: "2026-10-10T00:00:00Z"
toc: true
---

Put guardrails in code, not in the prompt.

- **Argument checks.** Reject a `minutes` value outside 1 to 1440 before the tool runs. Return the error text to the model.
- **Allowlist.** Each agent has a fixed set of tool names. Reject any other name.
- **Loop detection.** Chapter 6 built it. The run stops with `LOOP_DETECTED` when one tool name plus arguments repeats three times.

<figure class="flow">
<script type="application/json">
{
  "title": "Three guardrails between a tool call and the tool.",
  "steps": [
    {"label": "The model asks for a tool call"},
    {"label": "Is the tool name in this agent's allowlist?", "no": "Reject the name"},
    {"label": "Is minutes between 1 and 1440?", "no": "Return the error text to the model"},
    {"label": "Has this name plus arguments repeated fewer than three times?", "no": "Stop: LOOP_DETECTED"},
    {"label": "Run the tool", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 7.1. The three guardrails, in front of every tool. Each one is a line of Java, so the model cannot talk its way past it.</figcaption>
</figure>
