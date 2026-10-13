---
title: "Chapter 14: Skills as files"
linktitle: "14. Skills as files"
summary: "A SKILL.md per skill. Names and descriptions load at the start; full text loads on demand."
weight: 150

date: "2026-10-10T00:00:00Z"
toc: true
---

A skill is a folder with a `SKILL.md` file. The file has a name and a one-line description in front matter, then the full instructions. The harness loads only names and descriptions at the start. A `useSkill` tool loads the full text when the model asks for it.

```markdown
---
name: triage-error-group
description: Judge the severity of one error group from its rate, the services it affects, and whether a runbook exists.
---

# Steps
1. Read the error rate for the last 15 minutes.
2. List the affected services.
3. Search runbooks for the error fingerprint.
4. Return one severity: low, medium, or critical.
```

<figure class="seq">
<script type="application/json">
{
  "title": "Progressive loading: front matter first, full text on demand.",
  "lifelines": [
    {"id": "files", "label": "SKILL.md files", "tone": "platform"},
    {"id": "harness", "label": "Harness", "tone": "platform"},
    {"id": "model", "label": "Model", "tone": "subscriber"}
  ],
  "messages": [
    {"from": "harness", "to": "files", "label": "at start: read name + description only"},
    {"from": "harness", "to": "model", "label": "prompt lists triage-error-group and its description"},
    {"from": "model", "to": "harness", "label": "tool call: useSkill(triage-error-group)", "kind": "response"},
    {"from": "harness", "to": "files", "label": "load the full SKILL.md"},
    {"from": "harness", "to": "model", "label": "tool result: steps 1 to 4"},
    {"from": "model", "to": "harness", "label": "follows the steps; returns low, medium, or critical", "kind": "response"}
  ]
}
</script>
<figcaption>Figure 14.1. A skill costs one line of the prompt until the model asks for it. The figure leaves out the tool calls the model makes while following the steps.</figcaption>
</figure>
