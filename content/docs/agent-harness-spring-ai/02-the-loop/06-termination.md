---
title: "Chapter 6: Termination"
linktitle: "6. Termination"
summary: "Every run ends for one named reason, returned in a RunResult."
weight: 70

date: "2026-10-10T00:00:00Z"
toc: true
---

This chapter adds three stop rules to the loop: a token budget, a timeout, and loop detection.

**Objectives:**

- Name every way a run can end.
- Stop a run that costs too much, takes too long, or repeats itself.
- Trigger each stop reason on purpose.

The Chapter 5 loop stops on a final answer or after 5 steps. Five steps can still cost too much. One slow model call can still hold a request for minutes. A model can request the same call again and again. Each failure needs its own stop rule and its own name.

## Step 1: Name every stop reason

Add three values to `StopReason` in `RunResult.java`:

```java
package com.garageeducation.harness;

/**
 * The outcome of one agent run.
 *
 * <p>Every run returns one {@code RunResult}. The {@link StopReason} says why the run ended.
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
        STEP_LIMIT,

        /** The run used more than {@code MAX_TOKENS} tokens. */
        TOKEN_BUDGET,

        /** The run took longer than {@code TIMEOUT}. */
        TIMEOUT,

        /** The model requested the same tool call {@code MAX_REPEATS} times. */
        LOOP_DETECTED
    }
}
```

Table 6.1 lists each reason and the limit behind it.

| `StopReason` | Limit | Protects |
|---|---|---|
| `FINAL_ANSWER` | none | Nothing. The run succeeded. |
| `STEP_LIMIT` | `MAX_STEPS = 5` | Model calls per run |
| `TOKEN_BUDGET` | `MAX_TOKENS = 8_000` | Cost per run |
| `TIMEOUT` | `TIMEOUT = 60 s` | Time per run |
| `LOOP_DETECTED` | `MAX_REPEATS = 3` | Repeated identical tool calls |

<p class="caption">Table 6.1. The stop reasons and their limits. Chapter 9 adds <code>APPROVAL_TIMEOUT</code> and <code>REJECTED</code>.</p>

### What Spring AI stops on its own

`ToolCallingAdvisor` from Chapter 4 runs a loop too. Table 6.2 compares its stop rules with yours.

| `StopReason` | `ToolCallingAdvisor` (Chapter 4) | `AgentLoop` |
|---|---|---|
| `FINAL_ANSWER` | Stops when the reply has no tool calls | The same |
| `STEP_LIMIT` | No step cap. It caps tool calls: 40 per tool and 150 in total, per question. | 5 model calls |
| `TOKEN_BUDGET` | None. It adds up the tokens but never stops on them. | 8,000 tokens |
| `TIMEOUT` | None | 60 seconds |
| `LOOP_DETECTED` | In part. The per-tool cap stops the 41st call to one tool, whatever its arguments. | 3 identical calls: same tool, same arguments |

<p class="caption">Table 6.2. Spring AI's stop rules next to yours, with the Spring AI 2.0.1 defaults. (Source: Spring AI reference, <a href="https://docs.spring.io/spring-ai/reference/api/tools.html">Tool Calling</a>, Tool Call Limits.)</p>

- **The caps do not protect `/run`.** `AgentLoop` runs each tool itself through `ToolCallback.call`. Spring AI's `DefaultToolCallingManager` never sees those calls. Your limits are the only ones.
- **On a cap breach, Spring AI ends the run.** `ToolCallingAdvisor` returns the breach as the final reply. Its finish reason is `ToolCallLimitExceededException.FINISH_REASON`.
- **The caps are properties.** Set `spring.ai.tools.limits.max-calls-per-tool-default` and `spring.ai.tools.limits.max-total-tool-calls` in `application.yaml`. The value `-1` turns a cap off.

Spring AI has no token or time limit for the tool loop. A harness needs both, so you write them.

## Step 2: Check the rules in order

The loop checks the rules after each model reply. Figure 6.1 shows the order.

<figure class="flow">
<script type="application/json">
{
  "title": "Stop checks after each model reply.",
  "steps": [
    {"label": "A model reply arrives"},
    {"label": "Does it have tool calls?", "no": "FINAL_ANSWER"},
    {"label": "Tokens within MAX_TOKENS?", "no": "TOKEN_BUDGET"},
    {"label": "Before the deadline?", "no": "TIMEOUT"},
    {"label": "Each call seen fewer than MAX_REPEATS times?", "no": "LOOP_DETECTED"},
    {"label": "Run the tools"},
    {"label": "Steps left?", "no": "STEP_LIMIT"},
    {"label": "Send the next request", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 6.1. The order of the stop checks in <code>AgentLoop.run</code>. A final answer wins over every limit. No tool runs after a limit is crossed.</figcaption>
</figure>

- **The final answer comes first.** A finished answer is never thrown away.
- **The limits come before the tools.** A tool never runs after the run is over budget.
- **The step limit comes last.** The `for` loop checks it before the next model call.

This is the full `AgentLoop.java` in the repository. The new lines are the three constants, the three tracking variables, and the stop-rule block.

```java
package com.garageeducation.harness;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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

    /** The most tokens one run can use, summed over all model calls. */
    static final int MAX_TOKENS = 8_000;

    /** The longest one run can take. The loop checks it after each model call. */
    static final Duration TIMEOUT = Duration.ofSeconds(60);

    /** How often the model can request the same tool call before the run stops. */
    static final int MAX_REPEATS = 3;

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

        Map<String, Integer> seenCalls = new HashMap<>();
        Instant deadline = Instant.now().plus(TIMEOUT);
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

            // Stop rules, checked before any tool runs.
            if (tokens > MAX_TOKENS) {
                log.debug("[loop] Step {}: {} tokens is over MAX_TOKENS {}. Stop: TOKEN_BUDGET", step, tokens, MAX_TOKENS);
                return new RunResult(null, StopReason.TOKEN_BUDGET, step, tokens);
            }
            if (Instant.now().isAfter(deadline)) {
                log.debug("[loop] Step {}: past the {} deadline. Stop: TIMEOUT", step, TIMEOUT);
                return new RunResult(null, StopReason.TIMEOUT, step, tokens);
            }
            for (ToolCall call : reply.getToolCalls()) {
                String key = call.name() + call.arguments();
                int count = seenCalls.getOrDefault(key, 0) + 1;
                seenCalls.put(key, count);
                if (count >= MAX_REPEATS) {
                    log.debug("[loop] Step {}: {} {} requested {} times. Stop: LOOP_DETECTED", step, call.name(), call.arguments(), count);
                    return new RunResult(null, StopReason.LOOP_DETECTED, step, tokens);
                }
            }

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

Each rule needs one variable:

- **`tokens`** sums `getTotalTokens()` over every call. LM Studio reports usage in each response.
- **`deadline`** is the start time plus `TIMEOUT`. The loop compares it with the clock after each call.
- **`seenCalls`** counts each tool name plus its exact JSON arguments. The third identical call stops the run.

The timeout does not cut a slow model call short. It stops the run at the next check.

## Step 3: Trigger each reason

Lower one limit, restart the app, and ask one question. Put the limit back after each test. The Chapter 6 request in `requests/harness.http` lists every change.

```bash
curl -G http://localhost:8080/run --data-urlencode "input=how many error events in the checkout service in the last 15 minutes?"
```

Table 6.3 shows the results from one run with Gemma.

| Change | Result |
|---|---|
| none | `{"answer":"There were 412 error events in the checkout service over the last 15 minutes.","reason":"FINAL_ANSWER","steps":2,"tokens":447}` |
| `MAX_STEPS = 1` | `{"answer":null,"reason":"STEP_LIMIT","steps":1,"tokens":288}` |
| `MAX_TOKENS = 100` | `{"answer":null,"reason":"TOKEN_BUDGET","steps":1,"tokens":242}` |
| `TIMEOUT = Duration.ofMillis(1)` | `{"answer":null,"reason":"TIMEOUT","steps":1,"tokens":230}` |
| `MAX_REPEATS = 1` | `{"answer":null,"reason":"LOOP_DETECTED","steps":1,"tokens":232}` |

<p class="caption">Table 6.3. One limit lowered per run, with Gemma. Token counts vary between runs.</p>

Each stop logs its reason. This is the log for `MAX_TOKENS = 100`:

```text
00:16:01.359 DEBUG DispatcherServlet                        GET "/run?input=how+many+error+events+in+the+checkout+service+in+the+last+15+minutes%3F", parameters={masked}
00:16:01.360 DEBUG AgentLoop                                [loop] Start. Your code runs the tools. Question: how many error events in the checkout service in the last 15 minutes?
00:16:01.360 DEBUG AgentLoop                                [loop] Step 1/5: sending 2 messages to the model
00:16:02.437 INFO  ChatModelCompletionObservationHandler    Chat Model Completion:
[]
00:16:02.438 INFO  ChatModelPromptContentObservationHandler Chat Model Prompt Content:
["You are a careful assistant. Answer in two sentences or fewer.", "how many error events in the checkout service in the last 15 minutes?"]
00:16:02.438 DEBUG AgentLoop                                [loop] Step 1: model requested 1 tool call(s), 237 tokens so far
00:16:02.438 DEBUG AgentLoop                                [loop] Step 1: 237 tokens is over MAX_TOKENS 100. Stop: TOKEN_BUDGET
00:16:02.440 DEBUG DispatcherServlet                        Completed 200 OK
```

The run stops after step 1. No `your code runs` line follows, so no tool ran.

Put the time window in the question. Without it, Gemma can ask for the window in plain text. That reply is a `FINAL_ANSWER`, so no limit fires.

**Exercise:** Set `MAX_TOKENS = 400` and ask about checkout and search together. Predict the stop reason before you run it.

**Summary:** Every run now ends for one named reason. A final answer always wins. No tool runs after a limit is crossed. Chapter 7 checks each tool call before it runs.
