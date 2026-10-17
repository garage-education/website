---
title: "Progress, open items, and changelog"
linktitle: "Progress and changelog"
summary: "What is written, what still needs checking, and how the course changed."
weight: 20

date: "2026-10-10T00:00:00Z"
toc: true
---

## Progress checklist

- [x] Front matter and glossary
- [x] Part 1: Foundations (chapters 1 to 4)
- [x] Part 2: The Loop (chapters 5 to 9)
- [x] Part 3: Memory and Retrieval (chapters 10 to 13)
- [x] Part 4: Skills and Agents (chapters 14 to 18)
- [x] Part 5: Observability, Evaluation, and Cost (chapters 19 to 22)
- [x] Part 6: Durable Execution with Temporal (chapters 23 and 24)
- [x] Part 7: Capstone (chapter 25)

## Open items

- [ ] Confirm class names and annotations against the pinned versions. Several chapters are marked to verify.
- [ ] Add the fake log data set and runbook files to the course repository.
- [ ] Add an answer key for each chapter exercise.
- [ ] Confirm the BM25 index statement and the probe syntax (Ch. 11, 12).
- [ ] Confirm the reranker `/rerank` request shape (Ch. 13).
- [ ] Confirm the Temporal annotation packages and starter keys (Ch. 24).
- [ ] Switch Chapter 25 to `io.temporal:spring-ai` after a public release (PR #40 is open).

## Changelog

- v0.1: Table of contents.
- v0.2: Front matter, glossary, chapters 1 to 7.
- v0.3: Chapters 8 to 25.
- v0.4: Hybrid retrieval with VectorChord (keyword and vector, merged with RRF).
- v0.5: Local BGE-M3 embeddings. Plain JUnit evals. Spring Cache with Caffeine.
- v0.6: Approvals and run state in PostgreSQL. LM Studio embeddings. Skill pre-filtering.
- v0.7: Knowledge graph in Apache AGE. Reranker over REST.
- v0.8: Spring AI Session for short-term memory. LM Studio chat with Gemma.
- v0.9: Temporal required for every run.
- v1.0: Versions pinned. Chapter 25 uses plain Temporal activities. Version policy added.
- v1.1: Consolidated into one document. Spring Boot 4.1.1, Spring AI 2.0.1, Session 0.6.0, Temporal 1.35.0.
- v1.2: Chapters 2 to 4 match the course repository. Gradle build, `application.yaml`, `TestController`, Javadoc, and recorded replies.
- v1.3: Chapters 5 and 6 rewritten around the repository code. `askHaltToolCall` shows a tool call as data. `AgentLoop` and `RunResult` implement five stop reasons, each tested on Gemma. `requests/harness.http` holds every test request.
- v1.4: Lombok `@RequiredArgsConstructor` replaces hand-written constructors. `AiConfig` provides one shared `ChatClient`. `AgentLoop` uses plain loops in place of streams. Lombok pinned to 1.18.48 for Java 27.
- v1.5: Readable DEBUG logs. Spring AI logs each prompt, reply, and tool run; `[auto]`, `[halt]`, `[loop]`, and `[tool]` lines mark each path. Chapters 2 to 6 show real log excerpts. Actuator added for Spring AI observations.
- v1.6: Chapters 1 to 6 explain each Spring AI idea with diagrams redrawn from the Spring AI reference. Ch. 1: tool calling in six steps. Ch. 2: the chat model family. Ch. 3: message roles, the ChatModel conversion, and `.content()` as the call that sends the request. Ch. 4: advisors, the tool calling loop, and its sequence. Ch. 5: the recursive advisor, the tool call message classes, and `ToolCallingManager`. Ch. 6: Spring AI's own tool call limits. Glossary adds Advisor.
- v1.7 (this document): The Spring Boot code moves to the `java/` folder, to make room for a Python track. Existing clones: pull, then open `java/` in your IDE and run `./gradlew bootRun` from there. Chapters 2 to 6 add a Python track: every code sample has a Java tab and a Python tab, and `python/` holds the same app in LangChain 1.4 and FastAPI. Both apps answer every request in `requests/harness.http`.
