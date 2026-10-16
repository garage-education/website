---
title: "Chapter 2: Project setup"
linktitle: "2. Project setup"
summary: "A Spring Boot 4.1.1 project with the Web MVC and OpenAI starters, pointed at LM Studio."
weight: 30

date: "2026-10-10T00:00:00Z"
toc: true
---

This chapter builds a Spring Boot 4.1.1 project that talks to LM Studio.

**Objectives:**

- Build the project with Gradle.
- Point Spring AI at the Gemma and BGE-M3 models in LM Studio.
- Confirm Gemma returns tool calls.

<figure class="arch">
<script type="application/json">
{
  "title": "The project and what it talks to.",
  "nodes": [
    {"id": "app", "type": "boundary", "x": 0, "y": 0, "w": 420, "h": 250, "label": "Spring Boot 4.1.1 app · Java 27 toolchain"},
    {"id": "aibom", "x": 20, "y": 40, "w": 180, "label": "Spring AI BOM", "detail": "2.0.1", "tone": "muted"},
    {"id": "web", "x": 220, "y": 40, "w": 180, "label": "Web MVC starter", "detail": "HTTP on port 8080", "tone": "muted"},
    {"id": "openai", "x": 120, "y": 150, "w": 180, "label": "OpenAI starter", "detail": "ChatClient, embeddings", "tone": "platform"},
    {"id": "lm", "type": "boundary", "x": 490, "y": 0, "w": 260, "h": 250, "label": "LM Studio · localhost:1234/v1"},
    {"id": "gemma", "x": 530, "y": 50, "w": 180, "label": "Gemma", "detail": "google/gemma-4-12b-qat", "tone": "ai"},
    {"id": "bge", "x": 530, "y": 150, "w": 180, "label": "BGE-M3", "detail": "text-embedding-bge-m3", "tone": "ai"}
  ],
  "edges": [
    {"from": "openai", "to": "gemma", "label": "chat", "fromSide": "right", "toSide": "left", "animated": true},
    {"from": "openai", "to": "bge", "label": "embed", "fromSide": "right", "toSide": "left"}
  ]
}
</script>
<figcaption>Figure 2.1. The project and the local model server. The Session and Temporal starters come in Chapters 10 and 24.</figcaption>
</figure>

## Step 1: The build file

The project uses Gradle with the Kotlin DSL. Figure 2.1 shows its parts.

```kotlin
plugins {
	java
	id("org.springframework.boot") version "4.1.1"
	id("io.spring.dependency-management") version "1.1.7"
}

group = "com.garageeducation"
version = "0.0.1-SNAPSHOT"

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(27)
	}
}

repositories {
	mavenCentral()
}

extra["springAiVersion"] = "2.0.1"
// Spring Boot 4.1.1 manages Lombok 1.18.46, which fails on JDK 27. 1.18.48 adds JDK 27 support.
extra["lombok.version"] = "1.18.48"

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-webmvc")
	implementation("org.springframework.boot:spring-boot-starter-actuator")
	implementation("org.springframework.ai:spring-ai-starter-model-openai")

	compileOnly("org.projectlombok:lombok")
	annotationProcessor("org.projectlombok:lombok")

	developmentOnly("org.springframework.boot:spring-boot-devtools")

	testImplementation("org.springframework.boot:spring-boot-starter-test")
	testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

dependencyManagement {
	imports {
		mavenBom("org.springframework.ai:spring-ai-bom:${property("springAiVersion")}")
	}
}

tasks.withType<Test> {
	useJUnitPlatform()
}
```

- `spring-ai-bom` pins every Spring AI module to 2.0.1.
- `spring-boot-starter-webmvc` serves HTTP on port 8080.
- `spring-boot-starter-actuator` turns on Micrometer observations. Spring AI uses them to log each prompt and reply.
- `spring-ai-starter-model-openai` creates the `ChatClient.Builder`.
- Lombok writes repeated Java code for you, such as constructors. It runs at compile time only.
- `lombok.version` pins Lombok 1.18.48. Spring Boot 4.1.1 picks 1.18.46, which fails to compile on Java 27.
- DevTools restarts the app when compiled classes change. It never ships in the final JAR.
- The toolchain is Java 27. Spring Boot 4.1.1 needs Java 17 or later.

In IntelliJ IDEA, accept the prompt to enable annotation processing. Lombok needs it.

`settings.gradle.kts` holds one line:

```kotlin
rootProject.name = "harness"
```

## Step 2: The model settings

LM Studio exposes an OpenAI-compatible API (application programming interface). The OpenAI starter calls it. Put the settings in `src/main/resources/application.yaml`.

```yaml
spring:
  application:
    name: harness
  ai:
    openai:
      base-url: http://localhost:1234/v1
      api-key: lm-studio
      chat:
        model: google/gemma-4-12b-qat
      embedding:
        model: text-embedding-bge-m3
    chat:
      observations:
        # Log every prompt sent to the model and every reply. Local and fake data only:
        # in production these logs can contain user data.
        log-prompt: true
        log-completion: true

logging:
  pattern:
    # Time, level, short class name, message. Easier to read than the default line.
    console: "%d{HH:mm:ss.SSS} %-5level %-40logger{0} %msg%n"
  level:
    # Our code: one line per decision in Assistant, AgentLoop, and LogTools.
    com.garageeducation.harness: DEBUG
    # Each HTTP request: "GET /run?input=...", then "Completed 200 OK".
    org.springframework.web.servlet.DispatcherServlet: DEBUG
    # Spring AI runs a tool: "Executing tool call: countErrors" (ChatClient path only).
    org.springframework.ai.model.tool.DefaultToolCallingManager: DEBUG
```

- `base-url` ends in `/v1`.
- LM Studio ignores the API key. The starter still needs a value.
- Each model name must match an identifier in LM Studio.
- `log-prompt` and `log-completion` print each prompt and each reply. Spring AI warns at startup, because real prompts can hold private data. This course uses fake data only.
- `logging.level` turns on DEBUG logs for our code and three Spring classes. Table 2.1 lists what each line means.

| Log line starts with | Written by | Means |
|---|---|---|
| `GET "/…"` and `Completed 200 OK` | Spring `DispatcherServlet` | One HTTP request starts and ends |
| `Chat Model Prompt Content` | Spring AI observation | The messages sent to the model, as text |
| `Chat Model Completion` | Spring AI observation | The model's reply text. `[]` means a tool call with no text. |
| `Executing tool call` | Spring AI `DefaultToolCallingManager` | Spring AI ran a tool for you |
| `[auto]` | `Assistant.askAutoToolCall` | The Chapter 4 path: Spring AI runs the tools |
| `[halt]` | `Assistant.askHaltToolCall` | The Chapter 5 path: no tool runs |
| `[loop]` | `AgentLoop.run` | One step or one stop decision of your loop |
| `[tool]` | `LogTools.countErrors` | The tool ran, with its arguments and result |

<p class="caption">Table 2.1. How to read the console log. Each chapter shows the lines its run prints.</p>

List the identifiers with this request:

```bash
curl http://localhost:1234/v1/models
```

## Step 3: The main class

```java
package com.garageeducation.harness;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Starts the harness.
 *
 * <p>Spring Boot scans this package and creates every bean in it.
 * The OpenAI starter adds a {@code ChatClient.Builder} for LM Studio.
 *
 * <p>The {@code main} method is package-private and {@code static}.
 * Java 25 and later accept this form.
 */
@SpringBootApplication
public class HarnessApplication {

	/**
	 * Runs the Spring Boot application on port 8080.
	 *
	 * @param args command-line arguments, passed to Spring Boot
	 */
	static void main(String[] args) {
		SpringApplication.run(HarnessApplication.class, args);
	}

}
```

Start the app:

```bash
./gradlew bootRun
```

On Windows, run `gradlew.bat bootRun`.

## Step 4: The pre-flight check

Send one request with a tool definition to Gemma. Confirm the response contains a tool call. Figure 2.2 shows the decision.

Every request in this course is in `requests/harness.http`. Open it in IntelliJ IDEA or in VS Code with the REST Client extension, then click the run icon next to a request. Run the two Chapter 2 requests. The pre-flight reply must contain `"finish_reason": "tool_calls"`.

<figure class="flow">
<script type="application/json">
{
  "title": "The pre-flight check.",
  "steps": [
    {"label": "Send one request with a tool definition to Gemma"},
    {"label": "Does the response contain a tool call?", "no": "Do not start the course yet"},
    {"label": "Start Chapter 3", "tone": "platform"}
  ]
}
</script>
<figcaption>Figure 2.2. The pre-flight check. Every chapter from Chapter 4 on depends on the model returning tool calls.</figcaption>
</figure>

**Summary:** The app starts on port 8080 and reaches LM Studio. Chapter 3 sends the first question.
