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

`ChatClient` runs the tool for you. Its `ToolCallingAdvisor` sends the result back to the model and returns the final text. Chapter 5 turns the advisor off and runs the tool by hand.

## Step 3: Run it with the tool

Restart the app. Table 4.1 lists three questions and the replies from one run.

| Question | Reply |
|---|---|
| `how many error events?` | Please specify which service you would like to check and the time window (in minutes) for the error count. |
| `how many error events in search service?` | There were 3 error events in the search service in the last 10 minutes. |
| `how many error events in checkout service?` | There are currently 412 error events in the checkout service over the last 15 minutes. |

<p class="caption">Table 4.1. Replies from Gemma with the tool attached. Your wording will differ.</p>

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
