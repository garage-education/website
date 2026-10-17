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

Build one chat client and share it.

<div class="lang-tabs">
<div class="lang-tabs__bar" role="tablist" aria-label="Code language"><button type="button" role="tab" class="lang-tab" id="t1-java-tab" data-lang="java" aria-controls="t1-java" aria-selected="true">Java</button><button type="button" role="tab" class="lang-tab" id="t1-python-tab" data-lang="python" aria-controls="t1-python" aria-selected="false">Python</button></div>
<div class="lang-panel" role="tabpanel" id="t1-java" data-lang="java" data-label="Java" aria-labelledby="t1-java-tab">

The OpenAI starter provides a `ChatClient.Builder`, already pointed at LM Studio. Create `AiConfig.java`:

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

</div>
<div class="lang-panel" role="tabpanel" id="t1-python" data-lang="python" data-label="Python" aria-labelledby="t1-python-tab">

`ChatOpenAI` speaks the OpenAI API, so it can point at LM Studio. Create `ai_config.py`:

```python
"""Creates the objects that talk to the model."""

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from harness.application_properties import ApplicationProperties
from harness.observation_logging import ChatModelObservationHandler


class AiConfig:
    """Creates the objects that talk to the model.

    It plays the part of the Spring ``@Configuration`` class.
    """

    def __init__(self, properties: ApplicationProperties) -> None:
        self.properties = properties

    def chat_model(self) -> BaseChatModel:
        """Builds one chat model for the whole app.

        ``ChatOpenAI`` speaks the OpenAI API, so ``base_url`` points it at LM Studio.
        Every class that needs the model receives this object.

        Returns:
            the shared chat model
        """
        return ChatOpenAI(
            base_url=self.properties.base_url,
            api_key=SecretStr(self.properties.api_key),
            model=self.properties.chat_model,
            callbacks=[ChatModelObservationHandler(self.properties.log_prompt, self.properties.log_completion)],
        )
```

- `AiConfig` plays the part of a Spring `@Configuration` class. `chat_model()` plays the part of the `@Bean` method.
- `base_url`, `api_key`, and `model` come from `application.yaml`, through the `ApplicationProperties` from Chapter 2.
- `callbacks` attaches the Chapter 2 logging handler. It prints each prompt and reply.
- `create_app()` calls `chat_model()` once and passes the same object to every class that needs it. Step 3 shows it.

</div>
</div>

## Step 2: The Assistant

<div class="lang-tabs">
<div class="lang-tabs__bar" role="tablist" aria-label="Code language"><button type="button" role="tab" class="lang-tab" id="t2-java-tab" data-lang="java" aria-controls="t2-java" aria-selected="true">Java</button><button type="button" role="tab" class="lang-tab" id="t2-python-tab" data-lang="python" aria-controls="t2-python" aria-selected="false">Python</button></div>
<div class="lang-panel" role="tabpanel" id="t2-java" data-lang="java" data-label="Java" aria-labelledby="t2-java-tab">

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

</div>
<div class="lang-panel" role="tabpanel" id="t2-python" data-lang="python" data-label="Python" aria-labelledby="t2-python-tab">

Create `assistant.py`:

```python
"""Sends one question to the chat model and returns its text reply."""

import logging
from typing import Final

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

log: Final = logging.getLogger(__name__)


class Assistant:
    """Sends one question to the chat model and returns its text reply."""

    SYSTEM: Final = "You are a careful assistant. Answer in two sentences or fewer."

    def __init__(self, chat: BaseChatModel) -> None:
        self.chat = chat

    def ask_auto_tool_call(self, question: str) -> str:
        """Asks the model one question.

        The system message limits the reply to two sentences.

        Args:
            question: the user's question, in plain text

        Returns:
            the model's final text reply
        """
        log.debug("[auto] LangChain runs every tool call. Question: %s", question)
        answer = self.chat.invoke([SystemMessage(self.SYSTEM), HumanMessage(question)]).text
        log.debug("[auto] Final answer: %s", answer)
        return answer
```

- The constructor receives the chat model. `create_app()` passes it in, like Spring's constructor injection.
- `log` is one logger per module. Each `log.debug` line shows in the console.
- `SYSTEM` is a class constant. `Final` tells the type checker it never changes, like `static final`.
- `SystemMessage` sets the rules. `HumanMessage` carries the question.
- `.invoke(…)` sends the request and returns the reply as an `AIMessage`. `.text` returns its text.
- Your code never builds the HTTP request. Figure 3.1 shows the call. Step 4 shows what happens inside it.
- The name `ask_auto_tool_call` looks ahead. Chapter 4 adds tools, and a LangChain agent runs them for you.

</div>
</div>

## Step 3: The controller

<div class="lang-tabs">
<div class="lang-tabs__bar" role="tablist" aria-label="Code language"><button type="button" role="tab" class="lang-tab" id="t3-java-tab" data-lang="java" aria-controls="t3-java" aria-selected="true">Java</button><button type="button" role="tab" class="lang-tab" id="t3-python-tab" data-lang="python" aria-controls="t3-python" aria-selected="false">Python</button></div>
<div class="lang-panel" role="tabpanel" id="t3-java" data-lang="java" data-label="Java" aria-labelledby="t3-java-tab">

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

</div>
<div class="lang-panel" role="tabpanel" id="t3-python" data-lang="python" data-label="Python" aria-labelledby="t3-python-tab">

Create `test_controller.py`:

```python
"""Exposes Assistant over HTTP for manual tests."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from harness.assistant import Assistant


class TestController:
    """Exposes ``Assistant`` over HTTP for manual tests.

    It plays the part of the Spring ``@RestController``. Each ``add_api_route`` line plays
    the part of one ``@GetMapping``.

    Example: ``GET http://localhost:8080/askAutoToolCall?input=how many error events?``
    """

    def __init__(self, assistant: Assistant) -> None:
        self.assistant = assistant
        self.router = APIRouter()
        self.router.add_api_route("/askAutoToolCall", self.ask_auto_tool_call, response_class=PlainTextResponse)

    def ask_auto_tool_call(self, input: str) -> str:
        """Sends the ``input`` query parameter to the model.

        Args:
            input: the question; the request fails without it

        Returns:
            the model's text reply
        """
        return self.assistant.ask_auto_tool_call(input)
```

- `add_api_route` maps `GET /askAutoToolCall` to the method, like `@GetMapping`.
- FastAPI reads `input` from the query string because it is a plain parameter, like `@RequestParam`.
- `PlainTextResponse` returns the text as is, like a Spring `String` return value.

Wire the objects in `harness_application.py`. Replace `create_app()` from Chapter 2:

```python
def create_app() -> FastAPI:
    """Creates every object and wires them together.

    It plays the part of Spring's application context: one place builds each object once
    and passes it to the constructors that need it.

    Returns:
        the web app, with the ``TestController`` routes
    """
    properties = ApplicationProperties.load()
    chat = AiConfig(properties).chat_model()
    controller = TestController(Assistant(chat))
    app = FastAPI(title="harness")
    app.include_router(controller.router)
    return app
```

- Spring finds and builds each bean for you. In Python, `create_app()` builds each object in order and passes it on.
- Add the imports for `AiConfig`, `Assistant`, and `TestController` at the top of the file.

</div>
</div>

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

There are three ways to read the reply. Table 3.1 lists them.

<div class="lang-tabs">
<div class="lang-tabs__bar" role="tablist" aria-label="Code language"><button type="button" role="tab" class="lang-tab" id="t4-java-tab" data-lang="java" aria-controls="t4-java" aria-selected="true">Java</button><button type="button" role="tab" class="lang-tab" id="t4-python-tab" data-lang="python" aria-controls="t4-python" aria-selected="false">Python</button></div>
<div class="lang-panel" role="tabpanel" id="t4-java" data-lang="java" data-label="Java" aria-labelledby="t4-java-tab">

| Method | Returns | Used in |
|---|---|---|
| `.content()` | The reply text, as a `String` | Chapters 3 and 4 |
| `.chatResponse()` | The full `ChatResponse`: reply message, tool calls, and token counts | Chapters 5 and 6 |
| `.entity(Type.class)` | The reply parsed into a Java object | Not used yet |

</div>
<div class="lang-panel" role="tabpanel" id="t4-python" data-lang="python" data-label="Python" aria-labelledby="t4-python-tab">

| Call | Returns | Used in |
|---|---|---|
| `.invoke(messages).text` | The reply text, as a `str` | Chapters 3 and 4 |
| `.invoke(messages)` | The full `AIMessage`: text, `tool_calls`, and `usage_metadata` (token counts) | Chapters 5 and 6 |
| `.with_structured_output(Type).invoke(messages)` | The reply parsed into a Python object | Not used yet |

In Python, `.invoke(…)` sends the request. There is no separate `.call()` step.

</div>
</div>

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

<div class="lang-tabs">
<div class="lang-tabs__bar" role="tablist" aria-label="Code language"><button type="button" role="tab" class="lang-tab" id="t5-java-tab" data-lang="java" aria-controls="t5-java" aria-selected="true">Java</button><button type="button" role="tab" class="lang-tab" id="t5-python-tab" data-lang="python" aria-controls="t5-python" aria-selected="false">Python</button></div>
<div class="lang-panel" role="tabpanel" id="t5-java" data-lang="java" data-label="Java" aria-labelledby="t5-java-tab">

```text
00:15:18.392 DEBUG DispatcherServlet                        GET "/askAutoToolCall?input=how+many+error+events%3F", parameters={masked}
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

</div>
<div class="lang-panel" role="tabpanel" id="t5-python" data-lang="python" data-label="Python" aria-labelledby="t5-python-tab">

```text
16:07:14.640 DEBUG harness.assistant                        [auto] LangChain runs every tool call. Question: how many error events?
16:07:14.644 INFO  ChatModelPromptContent                   Chat Model Prompt Content:
['You are a careful assistant. Answer in two sentences or fewer.', 'how many error events?']
16:07:19.309 INFO  httpx2                                   HTTP Request: POST http://localhost:1234/v1/chat/completions "HTTP/1.1 200 OK"
16:07:19.315 INFO  ChatModelCompletion                      Chat Model Completion:
['Please provide the log or data you are referring to so I can count the events for you. I do not have any context yet to identify specific errors.']
16:07:19.315 DEBUG harness.assistant                        [auto] Final answer: Please provide the log or data you are referring to so I can count the events for you. I do not have any context yet to identify specific errors.
16:07:19.316 INFO  uvicorn.access                           127.0.0.1:55581 - "GET /askAutoToolCall?input=how%20many%20error%20events%3F HTTP/1.1" 200
```

- The prompt holds two messages: the system rules and your question. Figure 3.2 shows both.
- `httpx2` writes one line per model call. It is the HTTP client inside the OpenAI SDK.
- `uvicorn.access` writes one line when the request ends, with its status code.
- No `Executing tool call` line appears. The model has no tools yet.

</div>
</div>

A request without `input` fails: Spring returns 400 and FastAPI returns 422. The model is never called.

Or run the Chapter 3 request in `requests/harness.http`.

**Summary:** One question reaches Gemma and returns text. The model cannot read logs yet. Chapter 4 gives it a tool.
