---
title: "Chapter 3: The model call"
linktitle: "3. The model call"
summary: "One ChatClient call, from a question to a text reply, behind one HTTP endpoint."
weight: 40

date: "2026-10-10T00:00:00Z"
toc: true
---

This chapter sends one question to Gemma and returns its text reply.

**Objectives:**

- Create one shared `ChatClient`.
- Write the `Assistant` service.
- Expose it over HTTP with `TestController`.
- See what the model answers without tools.

## Step 1: The chat client

The OpenAI starter provides a `ChatClient.Builder`, already pointed at LM Studio. Build one client and share it. Create `AiConfig.java`:

```java
package com.garageeducation.harness;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Creates the beans that talk to the model.
 */
@Configuration
public class AiConfig {

    /**
     * Builds one {@link ChatClient} for the whole app.
     *
     * <p>The OpenAI starter provides the builder, already pointed at LM Studio.
     * Every class that needs the model receives this client.
     *
     * @param builder the {@link ChatClient.Builder} from the OpenAI starter
     * @return the shared chat client
     */
    @Bean
    ChatClient chatClient(ChatClient.Builder builder) {
        return builder.build();
    }
}
```

- `@Configuration` marks a class that creates objects for Spring.
- `@Bean` registers the returned `ChatClient`. Spring calls this method once at startup.
- Any class that asks for a `ChatClient` now receives this one.

## Step 2: The Assistant

```java
package com.garageeducation.harness;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * Sends one question to the chat model and returns its text reply.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class Assistant {

    private static final String SYSTEM = "You are a careful assistant. Answer in two sentences or fewer.";

    private final ChatClient chat;

    /**
     * Asks the model one question.
     *
     * <p>The system message limits the reply to two sentences.
     *
     * @param question the user's question, in plain text
     * @return the model's final text reply
     */
    public String askAutoToolCall(String question) {
        log.debug("[auto] Spring AI runs every tool call. Question: {}", question);
        String answer = chat.prompt()
                .system(SYSTEM)
                .user(question)
                .call()
                .content();
        log.debug("[auto] Final answer: {}", answer);
        return answer;
    }
}
```

- `@Service` tells Spring to create one `Assistant` at startup.
- `@Slf4j` comes from Lombok. It adds a `log` field. Each `log.debug` line shows in the console.
- `@RequiredArgsConstructor` comes from Lombok. It writes a constructor with one argument per `final` field. Spring calls it and passes the `ChatClient` from Step 1.
- `.system(…)` sets the rules. `.user(…)` sets the question.
- `.call()` picks a blocking call. It sends nothing yet.
- `.content()` sends the request and returns the reply as a `String`.
- Your code never builds the HTTP request. Figure 3.1 shows the call. Step 4 shows what happens inside it.
- The name `askAutoToolCall` looks ahead. Chapter 4 adds tools, and `ChatClient` runs them for you.

## Step 3: The controller

```java
package com.garageeducation.harness;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

/**
 * Exposes {@link Assistant} over HTTP for manual tests.
 *
 * <p>Example: {@code GET http://localhost:8080/askAutoToolCall?input=how many error events?}
 */
@RestController
@RequiredArgsConstructor
public class TestController {

    private final Assistant assistant;

    /**
     * Sends the {@code input} query parameter to the model.
     *
     * @param input the question; the request fails without it
     * @return the model's text reply
     */
    @GetMapping("/askAutoToolCall")
    public String askAutoToolCall(@RequestParam String input) {
        return assistant.askAutoToolCall(input);
    }
}
```

- `@RestController` turns each method's return value into the HTTP response.
- `@GetMapping("/askAutoToolCall")` maps `GET /askAutoToolCall` to the method.
- `@RequestParam` reads `input` from the query string.

<figure class="seq">
<script type="application/json">
{
  "title": "GET /askAutoToolCall?input=…: one model call.",
  "lifelines": [
    {"id": "http", "label": "TestController", "tone": "platform"},
    {"id": "code", "label": "Assistant.askAutoToolCall", "tone": "platform"},
    {"id": "client", "label": "ChatClient", "tone": "platform"},
    {"id": "model", "label": "Gemma", "tone": "subscriber"}
  ],
  "messages": [
    {"from": "http", "to": "code", "label": "askAutoToolCall(input)"},
    {"from": "code", "to": "client", "label": "prompt().system(…).user(question).call()"},
    {"from": "code", "to": "client", "label": ".content()"},
    {"from": "client", "to": "model", "label": "request in the provider format"},
    {"from": "model", "to": "client", "label": "reply text", "kind": "response"},
    {"from": "client", "to": "code", "label": "the reply as a String", "kind": "response"},
    {"from": "code", "to": "http", "label": "reply text", "kind": "response"}
  ]
}
</script>
<figcaption>Figure 3.1. One model call. <code>.call()</code> only prepares the request. <code>.content()</code> sends it. No tools are attached, so the model answers from its own text.</figcaption>
</figure>

## Step 4: Inside one call

`.system(…)` and `.user(…)` each add one message. Spring AI gives every message a role. Figure 3.2 shows the four roles.

<figure class="sketch">
<svg viewBox="0 0 900 250" role="img" aria-label="The four message roles: system, user, assistant, and tool, with the Spring AI class for each and its value in this chapter">
<style>
.mr-role{font:700 14px "Sora","Public Sans",sans-serif}
.mr-sent{fill:#0d2238}.mr-reply{fill:#7b3f98}.mr-later{fill:#9cacb8}
.mr-code{fill:#23394d;font:12px "IBM Plex Mono",ui-monospace,monospace}
.mr-code.later{fill:#9cacb8}
.mr-box-reply{fill:#f4ecf8;stroke:#7b3f98;stroke-width:1.6}
.mr-box-later{fill:#fff;stroke:#9cacb8;stroke-width:1.4;stroke-dasharray:5 4}
.mr-split{stroke:#d9e1e7;stroke-width:1.2}
.mr-bracket{fill:none;stroke:#526577;stroke-width:1.4}
.mr-edge{fill:#526577;font:italic 12px "Public Sans",sans-serif}
</style>
<path class="mr-bracket" d="M14,34 L14,22 L431,22 L431,34"/>
<text class="mr-edge" x="222" y="16" text-anchor="middle">the prompt: sent to the model</text>
<path class="mr-bracket" d="M454,34 L454,22 L651,22 L651,34"/>
<text class="mr-edge" x="552" y="16" text-anchor="middle">the reply</text>
<rect class="sk-box" x="10" y="40" width="205" height="200" rx="10"/>
<text class="mr-role mr-sent" x="24" y="66">SYSTEM</text>
<text class="mr-code" x="24" y="88">SystemMessage</text>
<text class="sk-sub" x="24" y="114">Sets the rules for</text>
<text class="sk-sub" x="24" y="130">every reply.</text>
<line class="mr-split" x1="10" y1="160" x2="215" y2="160"/>
<text class="sk-sub" x="24" y="182">In this chapter:</text>
<text class="mr-code" x="24" y="204">Answer in two</text>
<text class="mr-code" x="24" y="220">sentences or fewer.</text>
<rect class="sk-box" x="230" y="40" width="205" height="200" rx="10"/>
<text class="mr-role mr-sent" x="244" y="66">USER</text>
<text class="mr-code" x="244" y="88">UserMessage</text>
<text class="sk-sub" x="244" y="114">The question or</text>
<text class="sk-sub" x="244" y="130">command.</text>
<line class="mr-split" x1="230" y1="160" x2="435" y2="160"/>
<text class="sk-sub" x="244" y="182">In this chapter:</text>
<text class="mr-code" x="244" y="204">how many error</text>
<text class="mr-code" x="244" y="220">events?</text>
<rect class="mr-box-reply" x="450" y="40" width="205" height="200" rx="10"/>
<text class="mr-role mr-reply" x="464" y="66">ASSISTANT</text>
<text class="mr-code" x="464" y="88">AssistantMessage</text>
<text class="sk-sub" x="464" y="114">The model's reply.</text>
<text class="sk-sub" x="464" y="130">Can hold tool calls.</text>
<line class="mr-split" x1="450" y1="160" x2="655" y2="160"/>
<text class="sk-sub" x="464" y="182">In this chapter:</text>
<text class="mr-code" x="464" y="204">Please provide</text>
<text class="mr-code" x="464" y="220">the logs…</text>
<rect class="mr-box-later" x="670" y="40" width="220" height="200" rx="10"/>
<text class="mr-role mr-later" x="684" y="66">TOOL</text>
<text class="mr-code later" x="684" y="88">ToolResponseMessage</text>
<text class="sk-sub" x="684" y="114">A tool's result, sent</text>
<text class="sk-sub" x="684" y="130">back to the model.</text>
<line class="mr-split" x1="670" y1="160" x2="890" y2="160"/>
<text class="sk-sub" x="684" y="182">In this chapter:</text>
<text class="mr-code later" x="684" y="204">none. Chapter 4</text>
<text class="mr-code later" x="684" y="220">adds a tool.</text>
</svg>
<figcaption>Figure 3.2. The four message roles. This chapter sends two messages and gets one back. Redrawn and cut down from the Spring AI reference, <a href="https://docs.spring.io/spring-ai/reference/api/prompt.html">Prompts</a>.</figcaption>
</figure>

- **System** sets the rules for the whole conversation.
- **User** is the question. One prompt can hold many user messages.
- **Assistant** is the model's reply. Chapter 5 reads tool calls from it.
- **Tool** carries a tool result back to the model. Chapter 5 builds one by hand.

`ChatClient` puts the messages in a `Prompt` and hands it to the `ChatModel` from Chapter 2. Figure 3.3 shows what the `ChatModel` does with it.

<figure class="sketch">
<svg viewBox="0 0 900 340" role="img" aria-label="OpenAiChatModel converts the Prompt into an OpenAI JSON request, LM Studio runs Gemma, and OpenAiChatModel converts the JSON reply into a ChatResponse">
<defs>
<marker id="cv-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#087f79"/></marker>
</defs>
<style>
.cv-arrow{fill:none;stroke:#087f79;stroke-width:2.4}
.cv-zone{fill:#eaf4f3;stroke:#087f79;stroke-width:1.2;stroke-dasharray:6 4}
.cv-zone-label{fill:#087f79;font:700 14px "Sora","Public Sans",sans-serif}
.cv-ext{fill:#fbfcfd;stroke:#9cacb8;stroke-width:1.2;stroke-dasharray:6 4}
.cv-model{fill:#f4ecf8;stroke:#7b3f98;stroke-width:1.8}
.cv-model-label{fill:#7b3f98;font:700 14px "Public Sans",sans-serif}
.cv-row{fill:#fff;stroke:#d9e1e7;stroke-width:1.2}
.cv-code{fill:#23394d;font:12px "IBM Plex Mono",ui-monospace,monospace}
.cv-step{fill:#0d2238}
.cv-step-n{fill:#fff;font:700 12px "Public Sans",sans-serif;text-anchor:middle}
</style>
<!-- Prompt -->
<text class="sk-sub" x="10" y="44">built by ChatClient</text>
<rect class="sk-box" x="10" y="54" width="185" height="136" rx="10"/>
<text class="sk-label" x="24" y="78">Prompt</text>
<rect class="cv-row" x="22" y="90" width="161" height="26" rx="5"/>
<text class="cv-code" x="30" y="108">SystemMessage</text>
<rect class="cv-row" x="22" y="120" width="161" height="26" rx="5"/>
<text class="cv-code" x="30" y="138">UserMessage</text>
<rect class="cv-row" x="22" y="150" width="161" height="26" rx="5"/>
<text class="cv-code" x="30" y="168">options: model</text>
<!-- OpenAiChatModel -->
<rect class="cv-zone" x="230" y="30" width="440" height="170" rx="14"/>
<text class="cv-zone-label" x="250" y="56">OpenAiChatModel</text>
<rect class="sk-box" x="250" y="82" width="180" height="60" rx="10"/>
<text class="sk-label" x="340" y="108" text-anchor="middle">Convert to an</text>
<text class="sk-label" x="340" y="126" text-anchor="middle">OpenAI request</text>
<rect class="sk-box" x="470" y="82" width="180" height="60" rx="10"/>
<text class="sk-label" x="560" y="108" text-anchor="middle">Convert to a</text>
<text class="sk-label" x="560" y="126" text-anchor="middle">ChatResponse</text>
<!-- LM Studio -->
<rect class="cv-ext" x="230" y="226" width="440" height="104" rx="14"/>
<text class="sk-label" x="330" y="250">LM Studio</text>
<text class="cv-code" x="410" y="250">/v1/chat/completions</text>
<rect class="sk-box" x="250" y="268" width="120" height="46" rx="8"/>
<text class="sk-label" x="310" y="296" text-anchor="middle">JSON request</text>
<rect class="cv-model" x="390" y="268" width="120" height="46" rx="8"/>
<text class="cv-model-label" x="450" y="296" text-anchor="middle">Gemma</text>
<rect class="sk-box" x="530" y="268" width="120" height="46" rx="8"/>
<text class="sk-label" x="590" y="296" text-anchor="middle">JSON reply</text>
<!-- ChatResponse -->
<rect class="sk-box" x="705" y="54" width="185" height="136" rx="10"/>
<text class="sk-label" x="719" y="78">ChatResponse</text>
<rect class="cv-row" x="717" y="90" width="161" height="40" rx="5"/>
<text class="cv-code" x="725" y="106">Generation:</text>
<text class="cv-code" x="725" y="122">AssistantMessage</text>
<rect class="cv-row" x="717" y="136" width="161" height="40" rx="5"/>
<text class="cv-code" x="725" y="152">Metadata:</text>
<text class="cv-code" x="725" y="168">model, tokens</text>
<text class="sk-sub" x="705" y="214">.content() returns the</text>
<text class="sk-sub" x="705" y="230">text of the reply.</text>
<path class="cv-arrow" d="M195,112 L246,112" marker-end="url(#cv-head)"/>
<path class="cv-arrow" d="M310,142 L310,264" marker-end="url(#cv-head)"/>
<path class="cv-arrow" d="M370,291 L386,291" marker-end="url(#cv-head)"/>
<path class="cv-arrow" d="M510,291 L526,291" marker-end="url(#cv-head)"/>
<path class="cv-arrow" d="M590,268 L590,146" marker-end="url(#cv-head)"/>
<path class="cv-arrow" d="M650,112 L701,112" marker-end="url(#cv-head)"/>
<circle class="cv-step" cx="208" cy="163" r="10"/><text class="cv-step-n" x="208" y="167">1</text>
<circle class="cv-step" cx="292" cy="212" r="10"/><text class="cv-step-n" x="292" y="216">2</text>
<circle class="cv-step" cx="608" cy="212" r="10"/><text class="cv-step-n" x="608" y="216">3</text>
</svg>
<figcaption>Figure 3.3. One model call inside the <code>ChatModel</code>. Your code sees only the <code>Prompt</code> and the <code>ChatResponse</code>. Redrawn from the Spring AI reference, <a href="https://docs.spring.io/spring-ai/reference/api/chatmodel.html">Chat Model API</a>, for LM Studio.</figcaption>
</figure>

The numbers in Figure 3.3 match these steps:

1. **Options.** The starter reads the model name from `application.yaml` at startup. A request can override it with `.options(…)`. This course keeps the startup options.
2. **Convert the request.** `OpenAiChatModel` turns the `Prompt` into an OpenAI JSON request. LM Studio runs Gemma on it.
3. **Convert the reply.** `OpenAiChatModel` turns the JSON reply into a `ChatResponse`. It holds the reply message and metadata, such as token counts.

`.content()` is one of three ways to read the reply. Table 3.1 lists them.

| Method | Returns | Used in |
|---|---|---|
| `.content()` | The reply text, as a `String` | Chapters 3 and 4 |
| `.chatResponse()` | The full `ChatResponse`: reply message, tool calls, and token counts | Chapters 5 and 6 |
| `.entity(Type.class)` | The reply parsed into a Java object | Not used yet |

<p class="caption">Table 3.1. Three ways to read one reply. Each one sends the request.</p>

Between `ChatClient` and the `ChatModel` sits a chain of advisors. Chapter 4 explains it.

## Step 5: Run the first call

Restart the app. Send a question:

```bash
curl -G http://localhost:8080/askAutoToolCall --data-urlencode "input=how many error events?"
```

The model has no data. It asks for the logs:

```text
Please provide the logs or data you are referring to. Once you share them, I can count the error events for you.
```

The console log shows the same run:

```text
patcherServlet                        GET "/askAutoToolCall?input=how+many+error+events%3F", parameters={masked}
00:15:18.393 DEBUG Assistant                                [auto] Spring AI runs every tool call. Question: how many error events?
00:15:20.872 INFO  ChatModelCompletionObservationHandler    Chat Model Completion:
["Please provide the data or context you are referring to. I do not see any events listed in your message."]
00:15:20.872 INFO  ChatModelPromptContentObservationHandler Chat Model Prompt Content:
["You are a careful assistant. Answer in two sentences or fewer.", "how many error events?"]
00:15:20.874 DEBUG Assistant                                [auto] Final answer: Please provide the data or context you are referring to. I do not see any events listed in your message.
00:15:20.882 DEBUG DispatcherServlet                        Completed 200 OK
```

- The prompt holds two messages: the system rules and your question. Figure 3.2 shows both.
- No `Executing tool call` line appears. The model has no tools yet.

A request without `input` fails. The model is never called.

Or run the Chapter 3 request in `requests/harness.http`.

**Summary:** One question reaches Gemma and returns text. The model cannot read logs yet. Chapter 4 gives it a tool.
