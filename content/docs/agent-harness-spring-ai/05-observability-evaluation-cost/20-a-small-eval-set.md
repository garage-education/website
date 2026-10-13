---
title: "Chapter 20: A small eval set"
linktitle: "20. A small eval set"
summary: "Fixed inputs, expected properties, plain JUnit 5. Run before every change."
weight: 210

date: "2026-10-10T00:00:00Z"
toc: true
---

An eval case has fixed input and expected properties. Check the stop reason, whether an alert posted, and required phrases. Do not check exact text, because model output varies.

<figure class="flow">
<script type="application/json">
{
  "title": "One eval case.",
  "steps": [
    {"label": "Read the case JSON"},
    {"label": "Run the watcher on its fixed input"},
    {"label": "Is the stop reason the expected one?", "no": "Fail"},
    {"label": "Did an alert post, or not, as expected?", "no": "Fail"},
    {"label": "Are the required phrases present?", "no": "Fail"},
    {"label": "Pass", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 20.1. One eval case checks properties, never exact text. A case can pass with different wording on every run.</figcaption>
</figure>

Write these cases first: a duplicate that should be suppressed, a critical error that needs approval, a flood that hits the rate limit, a novel error with no runbook, and an empty window that ends with no model call.

| Case | What it proves |
| --- | --- |
| `duplicate-suppressed` | A duplicate is suppressed |
| `critical-needs-approval` | A critical error waits for approval |
| `flood-hits-rate-limit` | A flood hits the rate limit |
| novel error, no runbook | The watcher copes with a novel error that has no runbook |
| empty window | An empty window ends with no model call |

<p class="caption"><strong>Table 20.1.</strong> The first five cases. The last two have no case name in the code yet.</p>

```java
@ParameterizedTest
@ValueSource(strings = {"duplicate-suppressed", "critical-needs-approval", "flood-hits-rate-limit"})
void evalCase(String caseName) throws Exception {
    // read the case JSON, run the watcher, assert the expected properties
}
```

Run the eval before every change. Use plain JUnit 5.
