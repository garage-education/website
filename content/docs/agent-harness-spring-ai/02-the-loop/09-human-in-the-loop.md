---
title: "Chapter 9: Human-in-the-loop"
linktitle: "9. Human-in-the-loop"
summary: "A critical alert waits for a person, durably, for up to one hour."
weight: 100

date: "2026-10-10T00:00:00Z"
toc: true
---

A critical alert waits for a person. The workflow sets its state to awaiting approval and waits for an approval signal or a one-hour timer. Temporal stores the wait, so a restart does not lose it. Chapter 24 shows the code. Keep an audit row in PostgreSQL for each decision.

<figure class="seq">
<script type="application/json">
{
  "title": "Approval: wait, decide, and record.",
  "lifelines": [
    {"id": "wf", "label": "Watcher workflow", "tone": "operator"},
    {"id": "person", "label": "Person", "tone": "external"},
    {"id": "pg", "label": "PostgreSQL audit", "tone": "platform"},
    {"id": "alert", "label": "Alert channel", "tone": "external"}
  ],
  "messages": [
    {"from": "wf", "to": "wf", "label": "critical: state = awaiting approval"},
    {"from": "wf", "to": "wf", "label": "wait for a signal or a one-hour timer"},
    {"from": "wf", "to": "pg", "label": "Temporal stores the wait. A worker restart does not lose it.", "kind": "note"},
    {"from": "person", "to": "wf", "label": "approval signal"},
    {"from": "wf", "to": "pg", "label": "audit row for the decision"},
    {"from": "wf", "to": "alert", "label": "post the alert"},
    {"from": "wf", "to": "alert", "label": "No signal in one hour: stop with APPROVAL_TIMEOUT", "kind": "note"}
  ]
}
</script>
<figcaption>Figure 9.1. The approval path for a critical alert. A rejection writes the audit row and stops with <code>REJECTED</code>. How the person is notified is not covered here.</figcaption>
</figure>
