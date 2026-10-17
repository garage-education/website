---
title: "Chapter 4: Tools"
linktitle: "4. Tools"
summary: "A tool is a Java method. The model chooses it from its name and description alone."
weight: 50

date: "2026-10-10T00:00:00Z"
toc: true
---

This chapter gives the model one tool to count error events.

**Objectives:**

- Write `countErrors` as a Spring AI tool.
- Attach it to the `Assistant`.
- Compare replies with and without the tool.

A tool is a Java method. The model chooses tools from their names and descriptions alone. A vague description causes wrong choices.

## Step 1: The tool

```java
package com.garageeducation.harness;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import lombok.extern.slf4j.Slf4j;

/**
 * Log tools the model can call.
 *
 * <p>The model sees only the tool name, the {@link Tool} description, and each
 * {@link ToolParam} description. It never sees the method body.
 */
@Slf4j
@Component
public class LogTools {

    /**
     * Counts error log events for one service.
     *
     * <p>The data is fake. The {@code checkout} service returns 412. Every other service returns 3.
     *
     * @param service the service name, for example {@code checkout}
     * @param minutes the look-back window in minutes, from 1 to 1440; the fake data ignores it
     * @return the number of error events
     */
    @Tool(description = "Count error log events for one service in the last N minutes. Use this to check for a current error spike.")
    public int countErrors(@ToolParam(description = "Service name, for example checkout") String service,
                           @ToolParam(description = "Look-back window in minutes, from 1 to 1440") int minutes) {
        int count = "checkout".equals(service) ? 412 : 3; // fake data
        log.debug("[tool] countErrors(service={}, minutes={}) returned {}", service, minutes, count);
        return count;
    }
}
```

- `@Tool` names the method as a tool. Its description tells the model when to use it.
- `@ToolParam` describes each argument. The model fills them in.
- `@Component` makes `LogTools` a bean, so Spring can pass it to other classes.

Figure 4.1 shows what the model sees.

<figure class="sketch">
<svg viewBox="0 0 880 300" role="img" aria-label="What the model sees of a tool, and what it never sees">
<style>.sk-code{fill:#23394d;font:12px "IBM Plex Mono",ui-monospace,monospace}.sk-box.seen{stroke:#087f79}.sk-box.unseen{stroke:#9cacb8;stroke-dasharray:5 4}</style>
<rect class="sk-box seen" x="10" y="10" width="520" height="280" rx="10"/>
<text class="sk-label" x="30" y="42">What the model sees</text>
<text class="sk-sub" x="30" y="78">name</text>
<text class="sk-code" x="150" y="78">countErrors</text>
<text class="sk-sub" x="30" y="112">description</text>
<text class="sk-code" x="150" y="112">Count error log events for one service</text>
<text class="sk-code" x="150" y="132">in the last N minutes. Use this to check</text>
<text class="sk-code" x="150" y="152">for a current error spike.</text>
<text class="sk-sub" x="30" y="188">service</text>
<text class="sk-code" x="150" y="188">Service name, for example checkout</text>
<text class="sk-sub" x="30" y="222">minutes</text>
<text class="sk-code" x="150" y="222">Look-back window in minutes, from 1 to 1440</text>
<text class="sk-sub" x="30" y="268">This is all it has to choose with.</text>
<rect class="sk-box unseen" x="560" y="10" width="310" height="280" rx="10"/>
<text class="sk-label" x="580" y="42">What it never sees</text>
<text class="sk-sub" x="580" y="78">the method body</text>
<text class="sk-code" x="580" y="112">return "checkout".equals(service)</text>
<text class="sk-code" x="580" y="132">    ? 412 : 3; // fake data</text>
<text class="sk-sub" x="580" y="188">the class name</text>
<text class="sk-code" x="580" y="222">LogTools</text>
</svg>
<figcaption>Figure 4.1. A tool, as the model sees it. A vague description on the left means a wrong choice, however good the code on the right is.</figcaption>
</figure>

## Step 2: Attach the tool

Make two changes to the `Assistant` from Chapter 3:

- Add a `private final LogTools logTools;` field. Lombok adds it to the constructor, and Spring passes in the bean.
- Pass the tools with `.tools(logTools)`.

```java
@Slf4j
@Service
@RequiredArgsConstructor
public class Assistant {

    private static final String SYSTEM = "You are a careful assistant. Answer in two sentences or fewer.";

    private final ChatClient chat;
    private final LogTools logTools;

    /**
     * Asks the model one question and lets {@link ChatClient} run the tools.
     *
     * <p>{@link ChatClient} registers a {@code ToolCallingAdvisor} by default. The advisor runs each
     * tool call, sends the result back to the model, and repeats until the reply has no tool calls.
     *
     * @param question the user's question, in plain text
     * @return the model's final text reply
     */
    public String askAutoToolCall(String question) {
        log.debug("[auto] Spring AI runs every tool call. Question: {}", question);
        String answer = chat.prompt()
                .system(SYSTEM)
                .user(question)
                .tools(logTools)
                .call()
                .content();
        log.debug("[auto] Final answer: {}", answer);
        return answer;
    }
}
```

`ChatClient` runs the tool for you. It does so through an advisor. Step 3 explains advisors. Step 4 shows the tool loop.

## Step 3: Advisors

`ChatClient` does not send your request straight to the model. The request first passes through a chain of advisors. An advisor is a class that runs around the model call. It can change the request, change the reply, or skip the model call. Servlet filters work the same way around a controller.

Figure 4.2 shows one request through the chain.

<figure class="sketch">
<svg viewBox="0 0 900 360" role="img" aria-label="The advisor chain: the request passes through each advisor in order to the model, and the reply passes back through them in reverse order">
<defs>
<marker id="ac-head-in" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#ff7629"/></marker>
<marker id="ac-head-out" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#087f79"/></marker>
</defs>
<style>
.ac-in{fill:none;stroke:#ff7629;stroke-width:2.4}
.ac-out{fill:none;stroke:#087f79;stroke-width:2.4}
.ac-zone{fill:#f3f7f8;stroke:#9cacb8;stroke-width:1.2;stroke-dasharray:6 4}
.ac-zone-label{fill:#0d2238;font:700 14px "Sora","Public Sans",sans-serif}
.ac-optional{stroke-dasharray:5 4}
.ac-split{stroke:#d9e1e7;stroke-width:1.2;stroke-dasharray:4 3}
.ac-in-text{fill:#c2410c;font:12px "Public Sans",sans-serif}
.ac-out-text{fill:#087f79;font:12px "Public Sans",sans-serif}
.ac-model{fill:#f4ecf8;stroke:#7b3f98;stroke-width:1.8}
.ac-model-label{fill:#7b3f98;font:700 14px "Public Sans",sans-serif}
.ac-code{fill:#23394d;font:12px "IBM Plex Mono",ui-monospace,monospace}
.ac-step{fill:#0d2238}
.ac-step-n{fill:#fff;font:700 12px "Public Sans",sans-serif;text-anchor:middle}
</style>
<rect class="ac-zone" x="170" y="40" width="545" height="300" rx="14"/>
<text class="ac-zone-label" x="190" y="66">Advisor chain</text>
<text class="sk-sub" x="300" y="66">sorted by getOrder(): lower runs first on the way in</text>
<!-- Your code -->
<rect class="sk-box" x="10" y="130" width="130" height="150" rx="10"/>
<text class="sk-label" x="24" y="156">Assistant</text>
<text class="ac-code" x="24" y="178">.call()</text>
<text class="ac-code" x="24" y="266">.content()</text>
<!-- Advisor 1 -->
<rect class="sk-box" x="190" y="90" width="145" height="230" rx="10"/>
<text class="sk-label" x="204" y="114">ToolCalling</text>
<text class="sk-label" x="204" y="130">Advisor</text>
<line class="ac-split" x1="190" y1="218" x2="335" y2="218"/>
<text class="ac-in-text" x="204" y="196">before: reads or</text>
<text class="ac-in-text" x="204" y="210">changes the request</text>
<text class="ac-out-text" x="204" y="240">after: reads or</text>
<text class="ac-out-text" x="204" y="254">changes the reply</text>
<text class="sk-sub" x="204" y="306">added by ChatClient</text>
<!-- Advisor 2: optional -->
<rect class="sk-box ac-optional" x="370" y="90" width="145" height="230" rx="10"/>
<text class="sk-label" x="384" y="114">Your advisors</text>
<text class="sk-sub" x="384" y="130">logging, memory, …</text>
<line class="ac-split" x1="370" y1="218" x2="515" y2="218"/>
<text class="ac-in-text" x="384" y="196">before</text>
<text class="ac-out-text" x="384" y="240">after</text>
<text class="sk-sub" x="384" y="306">added by you</text>
<!-- Advisor 3: framework -->
<rect class="sk-box" x="550" y="90" width="145" height="230" rx="10"/>
<text class="sk-label" x="564" y="114">ChatModel</text>
<text class="sk-label" x="564" y="130">CallAdvisor</text>
<line class="ac-split" x1="550" y1="218" x2="695" y2="218"/>
<text class="ac-in-text" x="564" y="196">sends the prompt</text>
<text class="ac-out-text" x="564" y="240">returns the reply</text>
<text class="sk-sub" x="564" y="306">always last</text>
<!-- The model -->
<rect class="ac-model" x="750" y="150" width="130" height="130" rx="10"/>
<text class="ac-model-label" x="815" y="210" text-anchor="middle">Gemma</text>
<text class="sk-sub" x="815" y="230" text-anchor="middle">the model</text>
<!-- Request: left to right -->
<path class="ac-in" d="M140,172 L186,172" marker-end="url(#ac-head-in)"/>
<path class="ac-in" d="M335,172 L366,172" marker-end="url(#ac-head-in)"/>
<path class="ac-in" d="M515,172 L546,172" marker-end="url(#ac-head-in)"/>
<path class="ac-in" d="M695,172 L746,172" marker-end="url(#ac-head-in)"/>
<!-- Reply: right to left -->
<path class="ac-out" d="M750,262 L699,262" marker-end="url(#ac-head-out)"/>
<path class="ac-out" d="M550,262 L519,262" marker-end="url(#ac-head-out)"/>
<path class="ac-out" d="M370,262 L339,262" marker-end="url(#ac-head-out)"/>
<path class="ac-out" d="M190,262 L144,262" marker-end="url(#ac-head-out)"/>
<!-- Step numbers, matching the list under the figure -->
<circle class="ac-step" cx="163" cy="150" r="10"/><text class="ac-step-n" x="163" y="154">1</text>
<circle class="ac-step" cx="352" cy="150" r="10"/><text class="ac-step-n" x="352" y="154">2</text>
<circle class="ac-step" cx="722" cy="150" r="10"/><text class="ac-step-n" x="722" y="154">3</text>
<circle class="ac-step" cx="722" cy="284" r="10"/><text class="ac-step-n" x="722" y="288">4</text>
<circle class="ac-step" cx="352" cy="284" r="10"/><text class="ac-step-n" x="352" y="288">5</text>
<circle class="ac-step" cx="163" cy="284" r="10"/><text class="ac-step-n" x="163" y="288">6</text>
</svg>
<figcaption>Figure 4.2. The advisor chain. Orange is the request on the way in. Teal is the reply on the way out. Your advisors can sit before or after <code>ToolCallingAdvisor</code>, by their order. Redrawn from the Spring AI reference, <a href="https://docs.spring.io/spring-ai/reference/api/advisors.html">Advisors</a>.</figcaption>
</figure>

The numbers in Figure 4.2 match these steps:

1. **Wrap.** `ChatClient` wraps your prompt in a `ChatClientRequest`. The request carries an empty context map that advisors can share.
2. **Advise the request.** Each advisor reads or changes the request, then passes it to the next advisor.
3. **Call the model.** The last advisor, `ChatModelCallAdvisor`, sends the prompt to the model.
4. **Wrap the reply.** The model's reply comes back as a `ChatClientResponse`.
5. **Advise the reply.** Each advisor reads or changes the reply, in reverse order.
6. **Return.** `.content()` takes the text from the reply.

Each advisor implements one method. This is the interface in Spring AI 2.0.1:

```java
public interface CallAdvisor extends Advisor {
    ChatClientResponse adviseCall(ChatClientRequest request, CallAdvisorChain chain);
}
```

- **Code before `chain.nextCall(request)`** runs on the way in.
- **Code after it** runs on the way out.
- **An advisor that never calls `chain.nextCall`** skips the model. It must build the reply itself.
- **`getOrder()`** sets the position. The advisor with the lowest number sees the request first and the reply last.

Spring AI ships each common job as one advisor. Table 4.1 lists the built-in advisors.

| Advisor | Job | Course topic |
|---|---|---|
| `ToolCallingAdvisor` | Runs each tool call and sends the result back to the model | Chapter 4. Chapter 5 turns it off. |
| `MessageChatMemoryAdvisor` | Adds earlier messages of the conversation to the request | Memory, Chapter 10 |
| `QuestionAnswerAdvisor`, `RetrievalAugmentationAdvisor` | Add retrieved documents to the request | Retrieval, Chapter 12 |
| `SafeGuardAdvisor` | Blocks a request that contains listed words | Guardrails, Chapter 7 |
| `StructuredOutputValidationAdvisor` | Checks a JSON reply against a schema and retries on failure | |
| `SimpleLoggerAdvisor` | Logs each request and reply | Observability, Part 5 |

<p class="caption">Table 4.1. Built-in advisors in Spring AI 2.0.1. Each one adds a job without changing your model call.</p>

Add an advisor in one of two places:

- **On one request:** `.advisors(…)`, next to `.user(…)`.
- **On every request:** `.defaultAdvisors(…)` on the `ChatClient.Builder` in `AiConfig`.

The model call code stays the same. Memory, retrieval, and safety each plug into the same chain.

`ChatClient` adds `ToolCallingAdvisor` for you. Its order is `HIGHEST_PRECEDENCE + 300`, near the front of the chain. `MessageChatMemoryAdvisor` defaults to `HIGHEST_PRECEDENCE + 200`, so it runs before the tool loop starts. It saves the question and the final answer, not the tool steps. Step 4 shows why the order matters.

## Step 4: The tool calling loop

One `.call()` can reach the model more than once. `ToolCallingAdvisor` runs a loop until the model stops asking for tools. Figure 4.3 shows the loop.

<figure class="sketch">
<svg viewBox="0 0 900 470" role="img" aria-label="The tool calling loop: the ToolCallingAdvisor sends the messages to the model, runs each tool call, appends the result, and repeats until the reply has no tool call">
<defs>
<marker id="tl-head-main" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#ff7629"/></marker>
<marker id="tl-head-loop" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#087f79"/></marker>
<marker id="tl-head-def" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9cacb8"/></marker>
</defs>
<style>
.tl-main{fill:none;stroke:#ff7629;stroke-width:2.4}
.tl-loop{fill:none;stroke:#087f79;stroke-width:2.4}
.tl-def{fill:none;stroke:#9cacb8;stroke-width:1.6;stroke-dasharray:6 4}
.tl-zone{fill:#eaf4f3;stroke:#087f79;stroke-width:1.2;stroke-dasharray:6 4}
.tl-zone-label{fill:#087f79;font:700 14px "Sora","Public Sans",sans-serif}
.tl-loopbox{stroke:#087f79}
.tl-model{fill:#f4ecf8;stroke:#7b3f98;stroke-width:1.8}
.tl-model-label{fill:#7b3f98;font:700 14px "Public Sans",sans-serif}
.tl-row{fill:#fff;stroke:#d9e1e7;stroke-width:1.2}
.tl-row.new{fill:#eaf4f3;stroke:#087f79}
.tl-row.defs{stroke:#9cacb8;stroke-dasharray:4 3}
.tl-code{fill:#23394d;font:12px "IBM Plex Mono",ui-monospace,monospace}
.tl-code.loop{fill:#087f79}
.tl-edge{fill:#526577;font:italic 12px "Public Sans",sans-serif}
.tl-edge.loop{fill:#087f79}
.tl-edge.main{fill:#c2410c}
.tl-step{fill:#0d2238}
.tl-step-n{fill:#fff;font:700 12px "Public Sans",sans-serif;text-anchor:middle}
</style>
<!-- The ToolCallingAdvisor owns everything inside this zone -->
<rect class="tl-zone" x="200" y="62" width="690" height="338" rx="14"/>
<text class="tl-zone-label" x="220" y="88">ToolCallingAdvisor</text>
<text class="sk-sub" x="370" y="88">ChatClient adds it when a request has tools</text>
<!-- Your code -->
<rect class="sk-box" x="10" y="62" width="165" height="74" rx="10"/>
<text class="sk-label" x="24" y="88">LogTools</text>
<text class="tl-code" x="24" y="110">@Tool countErrors</text>
<text class="sk-sub" x="24" y="127">the tools you wrote</text>
<rect class="sk-box" x="10" y="262" width="165" height="62" rx="10"/>
<text class="sk-label" x="24" y="287">Assistant</text>
<text class="tl-code" x="24" y="308">askAutoToolCall()</text>
<path class="tl-def" d="M92,136 L92,256" marker-end="url(#tl-head-def)"/>
<text class="tl-edge" x="100" y="200">.tools(logTools)</text>
<!-- Main path: request in -->
<path class="tl-main" d="M175,293 L238,293" marker-end="url(#tl-head-main)"/>
<circle class="sk-box" cx="256" cy="293" r="16"/>
<text class="sk-label" x="256" y="298" text-anchor="middle">+</text>
<path class="tl-main" d="M272,293 L292,293" marker-end="url(#tl-head-main)"/>
<!-- The messages sent on each model call -->
<rect class="sk-box" x="296" y="200" width="196" height="186" rx="10"/>
<text class="sk-label" x="310" y="222">Messages sent</text>
<rect class="tl-row defs" x="308" y="232" width="172" height="26" rx="5"/>
<text class="tl-code" x="316" y="250">Tools: countErrors</text>
<rect class="tl-row" x="308" y="264" width="172" height="26" rx="5"/>
<text class="tl-code" x="316" y="282">System: rules</text>
<rect class="tl-row" x="308" y="296" width="172" height="26" rx="5"/>
<text class="tl-code" x="316" y="314">User: question</text>
<rect class="tl-row new" x="308" y="328" width="172" height="22" rx="5"/>
<text class="tl-code loop" x="316" y="344">AI: tool call</text>
<rect class="tl-row new" x="308" y="354" width="172" height="22" rx="5"/>
<text class="tl-code loop" x="316" y="370">Tool: 412</text>
<path class="tl-main" d="M492,293 L526,293" marker-end="url(#tl-head-main)"/>
<!-- The model -->
<rect class="tl-model" x="530" y="266" width="112" height="54" rx="10"/>
<text class="tl-model-label" x="586" y="292" text-anchor="middle">Gemma</text>
<text class="sk-sub" x="586" y="310" text-anchor="middle">decides</text>
<path class="tl-main" d="M642,293 L700,293" marker-end="url(#tl-head-main)"/>
<!-- Decision -->
<path class="sk-box" d="M760,253 L820,293 L760,333 L700,293 Z"/>
<text class="sk-label" x="760" y="290" text-anchor="middle">Tool</text>
<text class="sk-label" x="760" y="306" text-anchor="middle">call?</text>
<!-- Loop path: yes -->
<path class="tl-loop" d="M760,253 L760,172" marker-end="url(#tl-head-loop)"/>
<text class="tl-edge loop" x="768" y="222">yes</text>
<rect class="sk-box tl-loopbox" x="640" y="108" width="190" height="62" rx="10"/>
<text class="sk-label" x="654" y="133">ToolCallingManager</text>
<text class="sk-sub" x="654" y="153">finds and runs the tool</text>
<path class="tl-loop" d="M640,139 L498,139" marker-end="url(#tl-head-loop)"/>
<rect class="tl-row new" x="526" y="128" width="88" height="22" rx="5"/>
<text class="tl-code loop" x="536" y="144">Tool: 412</text>
<rect class="sk-box tl-loopbox" x="224" y="108" width="270" height="62" rx="10"/>
<text class="sk-label" x="238" y="133">Append to the history</text>
<text class="sk-sub" x="238" y="153">the tool call and its result</text>
<path class="tl-loop" d="M256,170 L256,271" marker-end="url(#tl-head-loop)"/>
<!-- ToolCallingManager calls your method -->
<path class="tl-loop" d="M735,108 L735,32 L130,32 L130,58" marker-end="url(#tl-head-loop)"/>
<text class="tl-edge loop" x="420" y="25" text-anchor="middle">find and call countErrors(checkout, 15)</text>
<!-- Main path: final answer out -->
<path class="tl-main" d="M820,293 L872,293 L872,432 L60,432 L60,330" marker-end="url(#tl-head-main)"/>
<text class="tl-edge main" x="846" y="285" text-anchor="middle">no</text>
<text class="tl-edge main" x="466" y="454" text-anchor="middle">final answer: .content() returns the text</text>
<!-- Step numbers, matching the list under the figure -->
<circle class="tl-step" cx="206" cy="270" r="10"/><text class="tl-step-n" x="206" y="274">1</text>
<circle class="tl-step" cx="670" cy="270" r="10"/><text class="tl-step-n" x="670" y="274">2</text>
<circle class="tl-step" cx="840" cy="139" r="10"/><text class="tl-step-n" x="840" y="143">3</text>
<circle class="tl-step" cx="872" cy="360" r="10"/><text class="tl-step-n" x="872" y="364">4</text>
</svg>
<figcaption>Figure 4.3. The tool calling loop. Orange is one request in and one answer out. Teal is the loop the advisor runs. Redrawn from the Spring AI reference, <a href="https://docs.spring.io/spring-ai/reference/api/tools.html">Tool Calling</a>, for the Log Incident Watcher.</figcaption>
</figure>

The numbers in Figure 4.3 match these steps:

1. **Send.** The advisor sends the messages and the tool definitions to the model. A tool definition holds the name, the description, and the parameters from Figure 4.1.
2. **Decide.** The model replies with text or with a tool call. A tool call names the tool and its arguments. It holds no answer.
3. **Run.** For a tool call, the advisor does three things:
   1. `ToolCallingManager` finds the matching tool and calls your method.
   2. The advisor appends the tool call and its result to the history.
   3. The advisor sends the longer history back to the model, at step 1.
4. **Return.** A reply with no tool call ends the loop. `.content()` returns its text to `Assistant`.

- **Your code calls `.call()` once.** The loop runs inside it. One question about `checkout` costs two model calls.
- **The model never runs code.** It asks. `ToolCallingManager` runs your method in your app.
- **The model keeps no state.** Each model call resends the full history. The list of messages grows by two per tool call.
- **Spring AI caps tool calls only.** `DefaultToolCallingManager` allows 40 calls per tool and 150 in total for each question. Nothing caps tokens or time. Chapter 6 adds those limits.
- **Order decides what runs inside the loop.** An advisor with a higher order than `ToolCallingAdvisor` runs on every model call. An advisor with a lower order runs once for each `.call()`.

Figure 4.4 shows the same run in time order, with the checkout question from Step 5.

<figure class="seq">
<script type="application/json">
{
  "title": "GET /askAutoToolCall: ToolCallingAdvisor runs the tool loop.",
  "lifelines": [
    {"id": "code", "label": "Assistant", "tone": "platform"},
    {"id": "advisor", "label": "ToolCallingAdvisor", "tone": "platform"},
    {"id": "model", "label": "Gemma", "tone": "subscriber"},
    {"id": "manager", "label": "ToolCallingManager", "tone": "platform"},
    {"id": "tools", "label": "LogTools", "tone": "platform"}
  ],
  "messages": [
    {"from": "code", "to": "advisor", "label": ".call(): system + user + tools"},
    {"from": "advisor", "to": "model", "label": "pass 1: system + user + countErrors definition"},
    {"from": "model", "to": "advisor", "label": "tool call: countErrors(checkout, 15)", "kind": "response"},
    {"from": "advisor", "to": "manager", "label": "executeToolCalls(prompt, reply)"},
    {"from": "manager", "to": "tools", "label": "countErrors(\"checkout\", 15)"},
    {"from": "tools", "to": "manager", "label": "412", "kind": "response"},
    {"from": "manager", "to": "advisor", "label": "history + tool call + result", "kind": "response"},
    {"from": "advisor", "to": "model", "label": "pass 2: system + user + tool call + result"},
    {"from": "model", "to": "advisor", "label": "text, no tool call", "kind": "response"},
    {"from": "advisor", "to": "code", "label": ".content(): the final text", "kind": "response"}
  ]
}
</script>
<figcaption>Figure 4.4. One <code>.call()</code>, two model calls. Your code sees only the first and last arrows. The figure leaves out <code>ChatModelCallAdvisor</code>, which carries each model call.</figcaption>
</figure>

- **Arrows 2 and 3** are the first model call. The log shows its completion as `[]`.
- **Arrows 4 to 7** are the tool run. The log shows `Executing tool call: countErrors`, then the `[tool]` line.
- **Arrows 8 and 9** are the second model call. Its prompt holds four messages.

Chapter 5 turns the advisor off. Your code then runs steps 3 and 4 itself. Compare Figure 4.4 with Figure 5.4 there.

## Step 5: Run it with the tool

Restart the app. Table 4.2 lists three questions and the replies from one run.

| Question | Reply |
|---|---|
| `how many error events?` | Please specify which service you would like to check and the time window (in minutes) for the error count. |
| `how many error events in search service?` | There were 3 error events in the search service in the last 10 minutes. |
| `how many error events in checkout service?` | There are currently 412 error events in the checkout service over the last 15 minutes. |

<p class="caption">Table 4.2. Replies from Gemma with the tool attached. Your wording will differ.</p>

- Without a service name, the model asks for one. It does not guess.
- The counts match the fake data: 412 for `checkout`, 3 for the rest.
- The model chose `minutes` itself: 10 and 15. The question gave no window.

Send the last question:

```bash
curl -G http://localhost:8080/askAutoToolCall --data-urlencode "input=how many error events in checkout service?"
```

The three Chapter 4 requests in `requests/harness.http` send all three questions.

Read the log for a question with a service and a window:

```text
00:15:45.254 DEBUG DispatcherServlet                        GET "/askAutoToolCall?input=how+many+error+events+in+the+checkout+service+in+the+last+15+minutes%3F", parameters={masked}
00:15:45.254 DEBUG Assistant                                [auto] Spring AI runs every tool call. Question: how many error events in the checkout service in the last 15 minutes?
00:15:47.501 INFO  ChatModelCompletionObservationHandler    Chat Model Completion:
[]
00:15:47.501 INFO  ChatModelPromptContentObservationHandler Chat Model Prompt Content:
["You are a careful assistant. Answer in two sentences or fewer.", "how many error events in the checkout service in the last 15 minutes?"]
00:15:47.501 DEBUG DefaultToolCallingManager                Executing tool call: countErrors
00:15:47.503 DEBUG LogTools                                 [tool] countErrors(service=checkout, minutes=15) returned 412
00:15:47.803 INFO  ChatModelCompletionObservationHandler    Chat Model Completion:
["There were 412 error events in the checkout service over the last 15 minutes."]
00:15:47.803 INFO  ChatModelPromptContentObservationHandler Chat Model Prompt Content:
["You are a careful assistant. Answer in two sentences or fewer.", "how many error events in the checkout service in the last 15 minutes?", "", ""]
00:15:47.804 DEBUG Assistant                                [auto] Final answer: There were 412 error events in the checkout service over the last 15 minutes.
00:15:47.804 DEBUG DispatcherServlet                        Completed 200 OK
```

- **Two model calls for one request.** The first reply is a tool call, so its completion is `[]`.
- **`Executing tool call: countErrors`** means Spring AI ran the tool. Your code did not.
- **`[tool]`** shows the arguments the model chose and the result.
- **The second prompt has four messages.** The two `""` entries are the tool call and the tool result. They hold data, not text.

**Exercise:** Rename the tool, then remove its description. Compare the model's choices each time.

**Summary:** One `@Tool` method lets the model answer from data. The description decides when the model calls it.
