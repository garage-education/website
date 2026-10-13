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
- v1.1 (this document): Consolidated into one document. Spring Boot 4.1.1, Spring AI 2.0.1, Session 0.6.0, Temporal 1.35.0.
