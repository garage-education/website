---
title: "Chapter 3: The model call"
linktitle: "3. The model call"
summary: "One ChatClient call, from a question to a text reply."
weight: 40

date: "2026-10-10T00:00:00Z"
toc: true
---

```java
@Service
public class Assistant {

    private final ChatClient chat;

    public Assistant(ChatClient.Builder builder) {
        this.chat = builder.build();
    }

    public String ask(String question) {
        return chat.prompt()
                .system("You are a careful assistant. Answer in two sentences or fewer.")
                .user(question)
                .call()
                .content();
    }
}
```

The `ChatClient.Builder` is created by Spring Boot when a model starter is on the classpath. The model replies in text. The client hides the request format.

<figure class="seq">
<script type="application/json">
{
  "title": "Assistant.ask: one model call.",
  "lifelines": [
    {"id": "code", "label": "Assistant.ask", "tone": "platform"},
    {"id": "client", "label": "ChatClient", "tone": "platform"},
    {"id": "model", "label": "Gemma", "tone": "subscriber"}
  ],
  "messages": [
    {"from": "code", "to": "client", "label": "prompt().system(…).user(question)"},
    {"from": "client", "to": "model", "label": ".call(): request in the provider format"},
    {"from": "model", "to": "client", "label": "reply text", "kind": "response"},
    {"from": "client", "to": "code", "label": ".content(): a String", "kind": "response"}
  ]
}
</script>
<figcaption>Figure 3.1. One model call. Your code never builds the HTTP request; the client does. No tools are attached yet, so the model can only answer from its own text.</figcaption>
</figure>
