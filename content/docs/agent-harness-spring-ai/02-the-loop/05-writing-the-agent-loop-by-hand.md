---
title: "Chapter 5: Writing the agent loop by hand"
linktitle: "5. The agent loop by hand"
summary: "Halt the tool call, read it as data, then run it yourself in a four-step loop."
weight: 60

date: "2026-10-10T00:00:00Z"
toc: true
---

This chapter replaces Spring AI's tool loop with one you write and control.

**Objectives:**

- Stop a tool call before it runs, and read it.
- Write the four-step agent loop.
- Return every run as a `RunResult` with one stop reason.

In Chapter 4, `ChatClient` ran the tool for you. Your code saw only the final text. A harness must see each tool call. It decides whether the call runs, and when the run stops.

## Step 1: Halt the tool call

`ChatClient` runs tools through an advisor, the `ToolCallingAdvisor`. `ChatClient` adds it to every request by default. Remove it, and the tool calls come back to your code.

Add this method to `Assistant`:

```java
/**
 * Asks the model one question and stops before any tool runs.
 *
 * <p>{@code toolCallingAdvisorAutoRegister(false)} removes the {@code ToolCallingAdvisor}.
 * The model still sees the tools. Its tool calls come back to this code as data.
 *
 * @param question the user's question, in plain text
 * @return the tool calls the model requested; empty when it answered in text
 */
public List<ToolCall> askHaltToolCall(String question) {
    log.debug("[halt] ToolCallingAdvisor is off. No tool will run. Question: {}", question);
    AssistantMessage reply = chat.prompt()
            .system(SYSTEM)
            .user(question)
            .tools(logTools)
            .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
            .call()
            .chatResponse()
            .getResult()
            .getOutput();
    if (reply.hasToolCalls()) {
        for (ToolCall call : reply.getToolCalls()) {
            log.debug("[halt] Model requested {} {}. Not run.", call.name(), call.arguments());
        }
    } else {
        log.debug("[halt] Model answered in text, with no tool call: {}", reply.getText());
    }
    return reply.getToolCalls();
}
```

- The request is the same as `askAutoToolCall`. One line differs: `.advisors(…)`.
- `.chatResponse()` returns the full response, not only the text.
- `getOutput()` returns the model's reply as an `AssistantMessage`.
- `getToolCalls()` lists the tools the model wants to run.

Add the endpoint to `TestController`:

```java
@GetMapping("/askHaltToolCall")
public List<ToolCall> askHaltToolCall(@RequestParam String input) {
    return assistant.askHaltToolCall(input);
}
```

Restart the app. Ask the Chapter 4 question:

```bash
curl -G http://localhost:8080/askHaltToolCall --data-urlencode "input=how many error events in checkout service?"
```

Gemma returns one tool call. Nothing ran:

```json
[{"id":"3EFxibX93b79PlmooqxhndVzdVWXnAlJ","type":"function","name":"countErrors","arguments":"{\"minutes\":60,\"service\":\"checkout\"}"}]
```

- A tool call is data: an id, a tool name, and JSON arguments.
- The model chose `minutes: 60`. The question gave no window. Your value will differ between runs.
- A question that needs no tool returns `[]`. Try `input=what is a harness?`.

The log ends after one model call:

```text
00:15:48.922 DEBUG DispatcherServlet                        GET "/askHaltToolCall?input=how+many+error+events+in+the+checkout+service+in+the+last+15+minutes%3F", parameters={masked}
00:15:48.923 DEBUG Assistant                                [halt] ToolCallingAdvisor is off. No tool will run. Question: how many error events in the checkout service in the last 15 minutes?
00:15:49.829 INFO  ChatModelCompletionObservationHandler    Chat Model Completion:
[]
00:15:49.830 INFO  ChatModelPromptContentObservationHandler Chat Model Prompt Content:
["You are a careful assistant. Answer in two sentences or fewer.", "how many error events in the checkout service in the last 15 minutes?"]
00:15:49.830 DEBUG Assistant                                [halt] Model requested countErrors {"minutes":15,"service":"checkout"}. Not run.
00:15:49.830 DEBUG DispatcherServlet                        Completed 200 OK
```

No `Executing tool call` line and no `[tool]` line appear. The tool never ran.

Your code now owns the call. It can run it, change it, or refuse it.

## Step 2: The RunResult

A run can end in more than one way. Return the reason with the answer. Create `RunResult.java`:

```java
package com.garageeducation.harness;

/**
 * The outcome of one agent run.
 *
 * @param answer the model's final text; {@code null} when the run stopped before a final answer
 * @param reason the reason the run stopped
 * @param steps  the number of model calls the run made
 * @param tokens the total tokens the run used, as reported by the model server
 */
public record RunResult(String answer, StopReason reason, int steps, int tokens) {

    /**
     * Why a run stopped. Each run stops for exactly one reason.
     */
    public enum StopReason {

        /** The model replied without tool calls. Its text is the answer. */
        FINAL_ANSWER,

        /** The run made {@code MAX_STEPS} model calls without a final answer. */
        STEP_LIMIT
    }
}
```

Chapter 6 adds three more reasons.

## Step 3: The loop

The loop has four steps. Figure 5.1 shows them.

<figure class="flow">
<script type="application/json">
{
  "title": "The agent loop.",
  "steps": [
    {"label": "1. Send the messages to the model"},
    {"label": "2. Does the reply have tool calls?", "no": "Return its text: FINAL_ANSWER"},
    {"label": "3. Run each tool"},
    {"label": "4. Add the results to the messages"},
    {"label": "Is step still ≤ MAX_STEPS?", "no": "Stop: STEP_LIMIT"},
    {"label": "Repeat from step 1", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 5.1. The four steps and the step cap. Chapter 6 adds three more stop rules.</figcaption>
</figure>

Create `AgentLoop.java`:

```java
package com.garageeducation.harness;

import java.util.ArrayList;
import java.util.List;

import org.springframework.ai.chat.client.AdvisorParams;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.AssistantMessage.ToolCall;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.ToolResponseMessage;
import org.springframework.ai.chat.messages.ToolResponseMessage.ToolResponse;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.support.ToolCallbacks;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.stereotype.Service;

import com.garageeducation.harness.RunResult.StopReason;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * The agent loop, written by hand.
 *
 * <p>Each step sends the full message list to the model. A reply without tool calls ends the run.
 * Otherwise, the loop runs each tool, adds the results to the messages, and repeats.
 *
 * <p>{@link ChatClient} runs tools by itself through its {@code ToolCallingAdvisor}.
 * This class turns that advisor off, so the model's tool calls come back to this code.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AgentLoop {

    /** The most model calls one run can make. */
    static final int MAX_STEPS = 5;


    private static final String SYSTEM = "You are a careful assistant. Answer in two sentences or fewer.";

    private final ChatClient chat;
    private final LogTools logTools;

    /**
     * Runs the loop for one question.
     *
     * @param question the user's question, in plain text
     * @return the answer, the stop reason, the step count, and the tokens used
     */
    public RunResult run(String question) {
        List<Message> messages = new ArrayList<>();
        messages.add(new SystemMessage(SYSTEM));
        messages.add(new UserMessage(question));

        int tokens = 0;
        log.debug("[loop] Start. Your code runs the tools. Question: {}", question);

        for (int step = 1; step <= MAX_STEPS; step++) {
            // 1. Send the messages to the model.
            log.debug("[loop] Step {}/{}: sending {} messages to the model", step, MAX_STEPS, messages.size());
            ChatResponse response = chat.prompt()
                    .messages(messages)
                    .tools(logTools)
                    .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
                    .call()
                    .chatResponse();
            AssistantMessage reply = response.getResult().getOutput();
            messages.add(reply);
            tokens += response.getMetadata().getUsage().getTotalTokens();

            // 2. A reply without tool calls is the answer.
            if (!reply.hasToolCalls()) {
                log.debug("[loop] Step {}: no tool calls. Stop: FINAL_ANSWER, {} tokens. Answer: {}", step, tokens, reply.getText());
                return new RunResult(reply.getText(), StopReason.FINAL_ANSWER, step, tokens);
            }
            log.debug("[loop] Step {}: model requested {} tool call(s), {} tokens so far", step, reply.getToolCalls().size(), tokens);

            // 3. Run each tool. 4. Add the results to the messages.
            List<ToolResponse> results = new ArrayList<>();
            for (ToolCall call : reply.getToolCalls()) {
                log.debug("[loop] Step {}: your code runs {} {}", step, call.name(), call.arguments());
                results.add(new ToolResponse(call.id(), call.name(), runTool(call)));
            }
            messages.add(ToolResponseMessage.builder().responses(results).build());
        }
        log.debug("[loop] Used all {} steps without a final answer. Stop: STEP_LIMIT", MAX_STEPS);
        return new RunResult(null, StopReason.STEP_LIMIT, MAX_STEPS, tokens);
    }

    /**
     * Runs one tool call and returns its result as text.
     *
     * <p>{@code ToolCallbacks.from} wraps each {@code @Tool} method in a {@link ToolCallback}.
     * The loop picks the callback whose name matches the call. An unknown name returns an
     * error text to the model instead of failing the run.
     *
     * @param call one tool call from the model's reply
     * @return the tool's result, or an error text for an unknown tool
     */
    private String runTool(ToolCall call) {
        for (ToolCallback tool : ToolCallbacks.from(logTools)) {
            if (tool.getToolDefinition().name().equals(call.name())) {
                return tool.call(call.arguments());
            }
        }
        log.warn("[loop] Model requested an unknown tool: {}", call.name());
        return "Unknown tool: " + call.name();
    }
}
```

Read the code in four parts:

- **The message list.** It starts with the system and user messages. Each step adds the reply and the tool results. The model has no memory, so each call resends the full list.
- **The model call.** It is the Step 1 request with `.messages(messages)` in place of `.system()` and `.user()`.
- **The tool results.** Each `ToolResponse` keeps the call's id, so the model can match each result to its request. All results go back in one `ToolResponseMessage`.
- **`runTool`.** `ToolCallbacks.from(logTools)` wraps each `@Tool` method in a `ToolCallback`. The loop finds the callback with the call's name. `tool.call(arguments)` parses the JSON arguments and runs `countErrors`.

Figure 5.2 shows one run.

<figure class="seq">
<script type="application/json">
{
  "title": "A two-step run through the loop.",
  "lifelines": [
    {"id": "loop", "label": "AgentLoop.run", "tone": "platform"},
    {"id": "model", "label": "Gemma", "tone": "subscriber"},
    {"id": "tools", "label": "LogTools", "tone": "platform"}
  ],
  "messages": [
    {"from": "loop", "to": "model", "label": "step 1: system + user"},
    {"from": "model", "to": "loop", "label": "AssistantMessage with a countErrors call", "kind": "response"},
    {"from": "loop", "to": "tools", "label": "tool.call(arguments)"},
    {"from": "tools", "to": "loop", "label": "412", "kind": "response"},
    {"from": "loop", "to": "loop", "label": "add ToolResponseMessage to messages"},
    {"from": "loop", "to": "model", "label": "step 2: system + user + reply + tool result"},
    {"from": "model", "to": "loop", "label": "AssistantMessage, no tool calls", "kind": "response"},
    {"from": "loop", "to": "loop", "label": "return RunResult(text, FINAL_ANSWER, 2, tokens)"}
  ]
}
</script>
<figcaption>Figure 5.2. A two-step run. Your loop runs the tool, not Spring AI. Step 2 resends every message from step 1.</figcaption>
</figure>

## Step 4: Run the loop

Add the endpoint to `TestController`. Spring returns the record as JSON.

```java
@GetMapping("/run")
public RunResult run(@RequestParam String input) {
    return agentLoop.run(input);
}
```

Add a `private final AgentLoop agentLoop;` field next to `assistant`. Lombok adds it to the constructor. Restart the app, then run:

```bash
curl -G http://localhost:8080/run --data-urlencode "input=how many error events in checkout service?"
```

```json
{"answer":"There were 412 error events in the checkout service over the last 15 minutes.","reason":"FINAL_ANSWER","steps":2,"tokens":727}
```

The log shows each step of your loop:

```text
00:15:50.946 DEBUG DispatcherServlet                        GET "/run?input=how+many+error+events+in+the+checkout+service+in+the+last+15+minutes%3F", parameters={masked}
00:15:50.946 DEBUG AgentLoop                                [loop] Start. Your code runs the tools. Question: how many error events in the checkout service in the last 15 minutes?
00:15:50.946 DEBUG AgentLoop                                [loop] Step 1/5: sending 2 messages to the model
00:15:52.071 INFO  ChatModelCompletionObservationHandler    Chat Model Completion:
[]
00:15:52.071 INFO  ChatModelPromptContentObservationHandler Chat Model Prompt Content:
["You are a careful assistant. Answer in two sentences or fewer.", "how many error events in the checkout service in the last 15 minutes?"]
00:15:52.071 DEBUG AgentLoop                                [loop] Step 1: model requested 1 tool call(s), 263 tokens so far
00:15:52.072 DEBUG AgentLoop                                [loop] Step 1: your code runs countErrors {"minutes":15,"service":"checkout"}
00:15:52.073 DEBUG LogTools                                 [tool] countErrors(service=checkout, minutes=15) returned 412
00:15:52.073 DEBUG AgentLoop                                [loop] Step 2/5: sending 4 messages to the model
00:15:52.368 INFO  ChatModelCompletionObservationHandler    Chat Model Completion:
["There were 412 error events in the checkout service in the last 15 minutes."]
00:15:52.368 INFO  ChatModelPromptContentObservationHandler Chat Model Prompt Content:
["You are a careful assistant. Answer in two sentences or fewer.", "how many error events in the checkout service in the last 15 minutes?", "", ""]
00:15:52.368 DEBUG AgentLoop                                [loop] Step 2: no tool calls. Stop: FINAL_ANSWER, 469 tokens. Answer: There were 412 error events in the checkout service in the last 15 minutes.
00:15:52.370 DEBUG DispatcherServlet                        Completed 200 OK
```

- **`Step 1/5: sending 2 messages`**, then **`sending 4 messages`.** The list grows by the reply and the tool result.
- **`your code runs countErrors`** replaces Spring's `Executing tool call` line from Chapter 4.
- **`Stop: FINAL_ANSWER`** names the reason the run ended.

The Chapter 5 requests in `requests/harness.http` cover every run in this chapter.

Table 5.1 compares the three endpoints for the same question.

| Endpoint | Who runs the tool | Returns | Log tag |
|---|---|---|---|
| `/askAutoToolCall` | Spring AI's `ToolCallingAdvisor` | The final text | `[auto]`, then `Executing tool call` |
| `/askHaltToolCall` | Nobody | The tool calls, unrun | `[halt] … Not run.` |
| `/run` | `AgentLoop.runTool` | A `RunResult`: answer, reason, steps, and tokens | `[loop] Step N: …` |

<p class="caption">Table 5.1. One question, three levels of control.</p>

A question with two services runs two tool calls in one step:

```json
{"answer":"Checkout is significantly worse right now with 412 errors compared to only 3 errors for search.","reason":"FINAL_ANSWER","steps":2,"tokens":480}
```

**Exercise:** Set `MAX_STEPS = 1`. Ask the checkout question again. The run stops after the first tool call:

```json
{"answer":null,"reason":"STEP_LIMIT","steps":1,"tokens":288}
```

Set it back to 5.

**Summary:** The loop sends messages, runs tools, and stops with a named reason. Your code sees every tool call. Chapter 6 adds the stop rules that protect cost and time.
