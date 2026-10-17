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

`ChatClient` runs tools through an advisor, the `ToolCallingAdvisor`. `ChatClient` adds it to every request that has tools. Chapter 4, Step 3 explains advisors. Remove this one, and the tool calls come back to your code.

`ToolCallingAdvisor` is a recursive advisor. It sends the request down the rest of the chain more than once. Figure 5.1 shows the chain with the advisor and without it.

<figure class="sketch">
<svg viewBox="0 0 900 410" role="img" aria-label="Left: ToolCallingAdvisor repeats the rest of the chain while the reply has tool calls. Right: with the advisor removed, one model call returns the tool calls to AgentLoop, and AgentLoop repeats">
<defs>
<marker id="ra-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0d2238"/></marker>
<marker id="ra-loop" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#087f79"/></marker>
</defs>
<style>
.ra-arrow{fill:none;stroke:#0d2238;stroke-width:2}
.ra-loop{fill:none;stroke:#087f79;stroke-width:2.4}
.ra-frame{fill:none;stroke:#087f79;stroke-width:1.4;stroke-dasharray:6 4}
.ra-adv{fill:#eaf4f3;stroke:#087f79;stroke-width:1.8}
.ra-gone{fill:#fff;stroke:#9cacb8;stroke-width:1.4;stroke-dasharray:5 4}
.ra-gone-text{fill:#9cacb8;font:650 13px "Public Sans",sans-serif}
.ra-gone-code{fill:#9cacb8;font:11px "IBM Plex Mono",ui-monospace,monospace}
.ra-strike{stroke:#9cacb8;stroke-width:1.4}
.ra-model{fill:#f4ecf8;stroke:#7b3f98;stroke-width:1.8}
.ra-model-label{fill:#7b3f98;font:700 14px "Public Sans",sans-serif}
.ra-title{fill:#0d2238;font:700 14px "Sora","Public Sans",sans-serif}
.ra-edge{fill:#087f79;font:italic 12px "Public Sans",sans-serif}
</style>
<!-- Left: Chapter 4, advisor on -->
<text class="ra-title" x="225" y="24" text-anchor="middle">Chapter 4: advisor on</text>
<rect class="sk-box" x="115" y="48" width="220" height="44" rx="10"/>
<text class="sk-label" x="225" y="75" text-anchor="middle">Assistant</text>
<rect class="ra-frame" x="95" y="106" width="260" height="278" rx="12"/>
<rect class="ra-adv" x="115" y="118" width="220" height="112" rx="10"/>
<text class="sk-label" x="127" y="138">ToolCallingAdvisor</text>
<rect class="sk-box" x="135" y="176" width="80" height="38" rx="8"/>
<text class="sk-label" x="175" y="200" text-anchor="middle">Before</text>
<rect class="sk-box" x="235" y="176" width="80" height="38" rx="8"/>
<text class="sk-label" x="275" y="200" text-anchor="middle">After</text>
<path class="sk-box" d="M275,146 L297,157 L275,168 L253,157 Z"/>
<text class="sk-label" x="275" y="162" text-anchor="middle">?</text>
<path class="ra-loop" d="M253,157 C205,157 175,158 175,172" marker-end="url(#ra-loop)"/>
<rect class="sk-box" x="115" y="252" width="220" height="40" rx="10"/>
<text class="sk-label" x="225" y="277" text-anchor="middle">ChatModelCallAdvisor</text>
<rect class="ra-model" x="115" y="326" width="220" height="44" rx="10"/>
<text class="ra-model-label" x="225" y="353" text-anchor="middle">Gemma</text>
<path class="ra-arrow" d="M175,92 L175,150"/>
<path class="ra-arrow" d="M175,214 L175,248" marker-end="url(#ra-head)"/>
<path class="ra-arrow" d="M175,292 L175,322" marker-end="url(#ra-head)"/>
<path class="ra-arrow" d="M275,326 L275,296" marker-end="url(#ra-head)"/>
<path class="ra-arrow" d="M275,252 L275,218" marker-end="url(#ra-head)"/>
<path class="ra-arrow" d="M275,176 L275,170" marker-end="url(#ra-head)"/>
<path class="ra-arrow" d="M275,146 L275,96" marker-end="url(#ra-head)"/>
<text class="sk-sub" x="225" y="402" text-anchor="middle">The dashed box repeats while the reply has tool calls.</text>
<!-- Right: Chapter 5, advisor off -->
<text class="ra-title" x="675" y="24" text-anchor="middle">Chapter 5: advisor off</text>
<rect class="sk-box" x="565" y="48" width="220" height="44" rx="10"/>
<text class="sk-label" x="675" y="75" text-anchor="middle">AgentLoop</text>
<path class="ra-loop" d="M785,60 C845,60 845,84 789,84" marker-end="url(#ra-loop)"/>
<text class="ra-edge" x="800" y="112">your loop</text>
<text class="ra-edge" x="800" y="128">repeats</text>
<rect class="ra-gone" x="565" y="118" width="220" height="112" rx="10"/>
<text class="ra-gone-text" x="675" y="146" text-anchor="middle">ToolCallingAdvisor</text>
<line class="ra-strike" x1="606" y1="142" x2="744" y2="142"/>
<text class="ra-gone-code" x="675" y="174" text-anchor="middle">removed by</text>
<text class="ra-gone-code" x="675" y="192" text-anchor="middle">toolCallingAdvisor</text>
<text class="ra-gone-code" x="675" y="208" text-anchor="middle">AutoRegister(false)</text>
<rect class="sk-box" x="565" y="252" width="220" height="40" rx="10"/>
<text class="sk-label" x="675" y="277" text-anchor="middle">ChatModelCallAdvisor</text>
<rect class="ra-model" x="565" y="326" width="220" height="44" rx="10"/>
<text class="ra-model-label" x="675" y="353" text-anchor="middle">Gemma</text>
<path class="ra-arrow" d="M590,92 L590,248" marker-end="url(#ra-head)"/>
<path class="ra-arrow" d="M590,292 L590,322" marker-end="url(#ra-head)"/>
<path class="ra-arrow" d="M760,326 L760,296" marker-end="url(#ra-head)"/>
<path class="ra-arrow" d="M760,252 L760,96" marker-end="url(#ra-head)"/>
<text class="sk-sub" x="675" y="402" text-anchor="middle">One model call. The tool calls come back unrun.</text>
</svg>
<figcaption>Figure 5.1. The same chain, with and without <code>ToolCallingAdvisor</code>. The <code>?</code> asks whether the reply has tool calls. Redrawn from the Spring AI reference, <a href="https://docs.spring.io/spring-ai/reference/api/advisors-recursive.html">Recursive Advisors</a>.</figcaption>
</figure>

- **Left:** `Before` sends the request down. `After` checks the reply. A tool call sends it back through `Before`, after the tool runs.
- **Right:** the request goes down once. The reply comes back with its tool calls. `AgentLoop` decides what to do next.

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

The loop has four steps. Figure 5.2 shows them.

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
<figcaption>Figure 5.2. The four steps and the step cap. Chapter 6 adds three more stop rules.</figcaption>
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

The loop reads two message types and builds one more. Figure 5.3 shows how a tool call and its result fit together.

<figure class="sketch">
<svg viewBox="0 0 900 300" role="img" aria-label="An AssistantMessage holds ToolCall records. A ToolResponseMessage holds ToolResponse records. Each ToolResponse repeats the id of its ToolCall">
<defs>
<marker id="mt-has" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10" fill="none" stroke="#0d2238" stroke-width="1.6"/></marker>
</defs>
<style>
.mt-line{fill:none;stroke:#0d2238;stroke-width:1.6}
.mt-id{fill:none;stroke:#087f79;stroke-width:2;stroke-dasharray:5 4}
.mt-reply{fill:#f4ecf8;stroke:#7b3f98;stroke-width:1.6}
.mt-tool{fill:#eaf4f3;stroke:#087f79;stroke-width:1.6}
.mt-ex{fill:#fbfcfd;stroke:#d9e1e7;stroke-width:1.2}
.mt-code{fill:#23394d;font:12px "IBM Plex Mono",ui-monospace,monospace}
.mt-hl{fill:#087f79;font:700 12px "IBM Plex Mono",ui-monospace,monospace}
.mt-edge{fill:#526577;font:italic 12px "Public Sans",sans-serif}
.mt-id-label{fill:#087f79;font:italic 12px "Public Sans",sans-serif}
</style>
<!-- Row 1: the reply -->
<rect class="mt-reply" x="10" y="20" width="250" height="110" rx="10"/>
<text class="sk-label" x="24" y="44">AssistantMessage</text>
<text class="sk-sub" x="24" y="62">the model's reply</text>
<text class="mt-code" x="24" y="88">hasToolCalls()</text>
<text class="mt-code" x="24" y="108">getToolCalls()</text>
<path class="mt-line" d="M260,75 L316,75" marker-end="url(#mt-has)"/>
<text class="mt-edge" x="288" y="67" text-anchor="middle">0..*</text>
<rect class="sk-box" x="320" y="20" width="250" height="110" rx="10"/>
<text class="sk-label" x="334" y="44">ToolCall</text>
<text class="mt-hl" x="334" y="68">id</text>
<text class="mt-code" x="334" y="86">type</text>
<text class="mt-code" x="334" y="104">name</text>
<text class="mt-code" x="334" y="122">arguments (JSON)</text>
<rect class="mt-ex" x="610" y="20" width="280" height="110" rx="10"/>
<text class="sk-sub" x="624" y="42">From the Step 1 log:</text>
<text class="mt-hl" x="624" y="66">id: 3EFxibX9…</text>
<text class="mt-code" x="624" y="84">type: function</text>
<text class="mt-code" x="624" y="102">name: countErrors</text>
<text class="mt-code" x="624" y="120">{"minutes":15,"service":"checkout"}</text>
<!-- Row 2: the result -->
<rect class="mt-tool" x="10" y="176" width="250" height="110" rx="10"/>
<text class="sk-label" x="24" y="200">ToolResponseMessage</text>
<text class="sk-sub" x="24" y="218">your code builds it</text>
<text class="mt-code" x="24" y="244">builder()</text>
<text class="mt-code" x="24" y="264">  .responses(list)</text>
<path class="mt-line" d="M260,231 L316,231" marker-end="url(#mt-has)"/>
<text class="mt-edge" x="288" y="223" text-anchor="middle">1..*</text>
<rect class="sk-box" x="320" y="176" width="250" height="110" rx="10"/>
<text class="sk-label" x="334" y="200">ToolResponse</text>
<text class="mt-hl" x="334" y="224">id</text>
<text class="mt-code" x="334" y="242">name</text>
<text class="mt-code" x="334" y="260">responseData</text>
<rect class="mt-ex" x="610" y="176" width="280" height="110" rx="10"/>
<text class="sk-sub" x="624" y="198">After runTool:</text>
<text class="mt-hl" x="624" y="222">id: 3EFxibX9…</text>
<text class="mt-code" x="624" y="240">name: countErrors</text>
<text class="mt-code" x="624" y="258">responseData: 412</text>
<!-- The id links them -->
<path class="mt-id" d="M445,130 L445,176"/>
<text class="mt-id-label" x="455" y="158">same id</text>
<path class="mt-id" d="M750,130 L750,176"/>
<text class="mt-id-label" x="760" y="158">same id</text>
</svg>
<figcaption>Figure 5.3. The tool call and the tool result, as Spring AI classes. Redrawn and cut down from the Spring AI reference, <a href="https://docs.spring.io/spring-ai/reference/api/prompt.html">Prompts</a> (Message API).</figcaption>
</figure>

- **`ToolCall`** comes from the model. Your code reads it. It never changes it.
- **`ToolResponse`** comes from your code. It copies the call's `id` and `name`, and adds the result.
- **One `ToolResponseMessage`** carries every result from one step.

Figure 5.4 shows one run. Compare it with Figure 4.4. `AgentLoop` takes the place of `ToolCallingAdvisor` and `ToolCallingManager`.

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
<figcaption>Figure 5.4. A two-step run. Your loop runs the tool, not Spring AI. Step 2 resends every message from step 1.</figcaption>
</figure>

### Spring AI's version of this loop

Spring AI ships a helper for steps 3 and 4: `ToolCallingManager`. The Spring AI reference drives the same loop with it:

```java
while (response.hasToolCalls()) {
    ToolExecutionResult result = toolCallingManager.executeToolCalls(prompt, response);
    prompt = new Prompt(result.conversationHistory(), chatOptions);
    response = chatModel.call(prompt);
}
```

(Source: Spring AI reference, [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html), 2.0.1.)

`executeToolCalls` runs every tool call in the reply. `conversationHistory()` returns the old messages plus the reply and the tool results. Table 5.1 compares it with `runTool`.

| | `AgentLoop.runTool` | `ToolCallingManager.executeToolCalls` |
|---|---|---|
| Finds the tool | Your `for` loop, by name | The manager, by name |
| Builds the next messages | Your code adds the reply and a `ToolResponseMessage` | Returns the full history |
| Runs | One call at a time, so your code can check each one | Every call in the reply at once |
| Call limits | None | 40 per tool and 150 in total |
| A tool throws an exception | The HTTP request fails | The error text goes back to the model |

<p class="caption">Table 5.1. Your <code>runTool</code> and Spring AI's helper. This course writes the steps by hand to show each one.</p>

- **Writing the loop by hand skips Spring AI's tool limits and error handling.** The Spring AI reference warns about this. Chapter 6 adds limits of your own.
- **Checking one call at a time** is what Chapter 7 needs. It checks each call before it runs.

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

Table 5.2 compares the three endpoints for the same question.

| Endpoint | Who runs the tool | Returns | Log tag |
|---|---|---|---|
| `/askAutoToolCall` | Spring AI's `ToolCallingAdvisor` | The final text | `[auto]`, then `Executing tool call` |
| `/askHaltToolCall` | Nobody | The tool calls, unrun | `[halt] … Not run.` |
| `/run` | `AgentLoop.runTool` | A `RunResult`: answer, reason, steps, and tokens | `[loop] Step N: …` |

<p class="caption">Table 5.2. One question, three levels of control.</p>

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
