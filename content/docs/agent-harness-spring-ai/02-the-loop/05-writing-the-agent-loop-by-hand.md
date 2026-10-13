---
title: "Chapter 5: Writing the agent loop by hand"
linktitle: "5. The agent loop by hand"
summary: "Four steps, repeated until the reply has no tool calls."
weight: 60

date: "2026-10-10T00:00:00Z"
toc: true
---

The loop has four steps. Send the messages to the model. If the reply has no tool calls, return its text. Otherwise run each tool, add the results to the messages, and repeat.

<figure class="flow">
<script type="application/json">
{
  "title": "The agent loop.",
  "steps": [
    {"label": "1. Send the messages to the model"},
    {"label": "2. Does the reply have tool calls?", "no": "Return its text: FINAL_ANSWER"},
    {"label": "3. Run each tool"},
    {"label": "4. Add the results to the messages"},
    {"label": "Is step still ≤ MAX_STEPS?", "no": "Stop: STEP_LIMIT (Chapter 6)"},
    {"label": "Repeat from step 1", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 5.1. The four steps, with the step cap from the code below. The other stop rules come in Chapter 6.</figcaption>
</figure>

Turn off automatic tool execution, so the code runs each tool itself.

```java
ToolCallingChatOptions options = ToolCallingChatOptions.builder()
        .toolCallbacks(ToolCallbacks.from(logTools))
        .internalToolExecutionEnabled(false)
        .build();

for (int step = 1; step <= MAX_STEPS; step++) {
    ChatResponse response = model.call(new Prompt(messages, options));
    AssistantMessage reply = response.getResult().getOutput();
    messages.add(reply);
    if (!reply.hasToolCalls()) {
        return new RunResult(reply.getText(), StopReason.FINAL_ANSWER, step);
    }
    // run each tool call, add ToolResponseMessage to messages
}
```

<figure class="seq">
<script type="application/json">
{
  "title": "A two-step run through the loop.",
  "lifelines": [
    {"id": "loop", "label": "Your loop", "tone": "platform"},
    {"id": "model", "label": "ChatModel", "tone": "subscriber"},
    {"id": "tools", "label": "LogTools", "tone": "platform"}
  ],
  "messages": [
    {"from": "loop", "to": "model", "label": "step 1: call(new Prompt(messages, options))"},
    {"from": "model", "to": "loop", "label": "AssistantMessage with a countErrors call", "kind": "response"},
    {"from": "loop", "to": "tools", "label": "run countErrors"},
    {"from": "tools", "to": "loop", "label": "412", "kind": "response"},
    {"from": "loop", "to": "loop", "label": "add ToolResponseMessage to messages"},
    {"from": "loop", "to": "model", "label": "step 2: call(new Prompt(messages, options))"},
    {"from": "model", "to": "loop", "label": "AssistantMessage, no tool calls", "kind": "response"},
    {"from": "loop", "to": "loop", "label": "return RunResult(text, FINAL_ANSWER, 2)"}
  ]
}
</script>
<figcaption>Figure 5.2. A two-step run. Because <code>internalToolExecutionEnabled(false)</code> is set, your loop runs the tool, not Spring AI. Each step resends the full message list.</figcaption>
</figure>

> **Verify:** Confirm the class names and builder methods for your Spring AI version. They change between releases.
