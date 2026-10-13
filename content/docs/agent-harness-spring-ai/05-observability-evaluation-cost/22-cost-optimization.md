---
title: "Chapter 22: Cost optimization"
linktitle: "22. Cost optimization"
summary: "Measure tokens first, then cache triage by fingerprint for ten minutes."
weight: 230

date: "2026-10-10T00:00:00Z"
toc: true
---

Measure tokens per run first. Then add a cache with Spring Cache and Caffeine, keyed by error fingerprint, with a ten-minute expiry. Clear it when a runbook changes. Redis can replace Caffeine later with no code change.

```java
@Cacheable(cacheNames = "triage", key = "#fingerprint", unless = "#result == null")
public TriageDecision triage(String fingerprint, String stackTrace) { ... }
```

<figure class="arch">
<script type="application/json">
{
  "title": "The triage cache.",
  "nodes": [
    {"id": "call", "x": 0, "y": 60, "w": 190, "label": "triage(fingerprint, …)", "tone": "platform"},
    {"id": "cache", "x": 260, "y": 60, "w": 220, "label": "Caffeine cache \"triage\"", "detail": "key = fingerprint · 10 min", "tone": "data"},
    {"id": "model", "x": 560, "y": 60, "w": 180, "label": "Model", "detail": "only on a miss", "tone": "ai"},
    {"id": "runbook", "x": 260, "y": 200, "w": 220, "label": "Runbook changes", "tone": "external"},
    {"id": "redis", "x": 560, "y": 200, "w": 180, "label": "Redis", "detail": "later, no code change", "tone": "muted"}
  ],
  "edges": [
    {"from": "call", "to": "cache", "label": "lookup"},
    {"from": "cache", "to": "model", "label": "miss", "animated": true},
    {"from": "runbook", "to": "cache", "label": "clear", "dashed": true},
    {"from": "redis", "to": "cache", "label": "can replace", "dashed": true, "fromSide": "left", "toSide": "right"}
  ]
}
</script>
<figcaption>Figure 22.1. A repeat fingerprint within ten minutes costs no tokens. A null result is never cached, so a failed triage is retried.</figcaption>
</figure>

Provider prompt caching does not apply to LM Studio, so skip that step. Each step must lower the token count in the eval run. Remove any step that does not.

<figure class="flow">
<script type="application/json">
{
  "title": "Keep a cost step only if it pays.",
  "steps": [
    {"label": "Measure tokens per run"},
    {"label": "Add one cost step"},
    {"label": "Did the eval run use fewer tokens?", "no": "Remove the step"},
    {"label": "Keep it", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 22.2. Every cost step has to show its saving in the eval run.</figcaption>
</figure>
