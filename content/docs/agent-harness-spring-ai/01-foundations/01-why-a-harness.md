---
title: "Chapter 1: Why a harness?"
linktitle: "1. Why a harness?"
summary: "A model only reads and writes text. The harness adds five jobs around it."
weight: 20

date: "2026-10-10T00:00:00Z"
toc: true
---

A model reads text and writes text. It cannot run code, read files, or remember past calls. The harness adds those abilities. It does five jobs. It sends the prompt. It reads the reply. It runs the tools the model asks for. It returns the tool results. It decides when the run stops.

<figure class="seq">
<script type="application/json">
{
  "title": "One harness run: the five jobs, in order.",
  "lifelines": [
    {"id": "you", "label": "Engineer", "tone": "external"},
    {"id": "harness", "label": "Harness", "tone": "platform"},
    {"id": "model", "label": "Model", "tone": "subscriber"},
    {"id": "tool", "label": "countErrors tool", "tone": "platform"}
  ],
  "messages": [
    {"from": "you", "to": "harness", "label": "Is checkout slow?"},
    {"from": "harness", "to": "model", "label": "Job 1: send the prompt and the tool list"},
    {"from": "model", "to": "harness", "label": "tool call: countErrors(checkout)", "kind": "response"},
    {"from": "harness", "to": "harness", "label": "Job 2: read the reply"},
    {"from": "harness", "to": "tool", "label": "Job 3: run the tool"},
    {"from": "tool", "to": "harness", "label": "412 errors", "kind": "response"},
    {"from": "harness", "to": "model", "label": "Job 4: return the tool result"},
    {"from": "model", "to": "harness", "label": "answer, based on the real count", "kind": "response"},
    {"from": "harness", "to": "harness", "label": "Job 5: no more tool calls, so stop"},
    {"from": "harness", "to": "you", "label": "answer", "kind": "response"}
  ]
}
</script>
<figcaption>Figure 1.1. One harness run, with each of the five jobs labelled. Use Previous and Next to step through it. The count of 412 is the fake data from Chapter 4.</figcaption>
</figure>

**Example.** Asked alone, a model can only guess whether checkout is slow. With a harness, the model calls a `countErrors` tool, reads the real count, and answers from that data.

**Objectives:** describe a model call, name the five harness jobs, and explain what the course builds.

## Tool calling, step by step

A model is frozen after training. It cannot read today's logs or call an API. Tool calling fixes this. The model asks for a tool, and the harness runs it. Figure 1.2 shows the six steps.

<figure class="sketch">
<svg viewBox="0 0 900 420" role="img" aria-label="Tool calling in six steps: the request carries the tool definition to the model, the model asks for a tool call, the harness runs the tool, sends the result back, and the model writes the final answer">
<defs>
<marker id="tc-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0d2238"/></marker>
</defs>
<style>
.tc-arrow{fill:none;stroke:#0d2238;stroke-width:2}
.tc-dot{fill:none;stroke:#526577;stroke-width:1.4;stroke-dasharray:2 4}
.tc-zone{fill:#eaf4f3;stroke:#087f79;stroke-width:1.2;stroke-dasharray:6 4}
.tc-zone-label{fill:#087f79;font:700 14px "Sora","Public Sans",sans-serif}
.tc-tool{fill:#eaf4f3;stroke:#087f79;stroke-width:1.8}
.tc-model{fill:#f4ecf8;stroke:#7b3f98;stroke-width:1.8}
.tc-model-label{fill:#7b3f98;font:700 15px "Public Sans",sans-serif}
.tc-def{fill:#eaf4f3;stroke:#087f79;stroke-width:1.2}
.tc-code{fill:#23394d;font:12px "IBM Plex Mono",ui-monospace,monospace}
.tc-edge{fill:#526577;font:italic 12px "Public Sans",sans-serif}
.tc-step{fill:#0d2238}
.tc-step-n{fill:#fff;font:700 12px "Public Sans",sans-serif;text-anchor:middle}
</style>
<!-- The tool -->
<rect class="tc-tool" x="320" y="10" width="260" height="62" rx="10"/>
<text class="sk-label" x="450" y="36" text-anchor="middle">countErrors</text>
<text class="sk-sub" x="450" y="56" text-anchor="middle">a Java method in your app</text>
<!-- The harness -->
<rect class="tc-zone" x="200" y="118" width="500" height="172" rx="14"/>
<text class="tc-zone-label" x="690" y="146" text-anchor="end">Harness</text>
<text class="sk-sub" x="690" y="164" text-anchor="end">Spring AI, or your own loop</text>
<rect class="sk-box" x="340" y="176" width="220" height="68" rx="10"/>
<text class="sk-label" x="450" y="206" text-anchor="middle">Dispatch tool calls</text>
<text class="sk-sub" x="450" y="226" text-anchor="middle">find the tool by name, run it</text>
<!-- The model -->
<rect class="tc-model" x="200" y="330" width="500" height="64" rx="10"/>
<text class="tc-model-label" x="450" y="358" text-anchor="middle">Gemma</text>
<text class="sk-sub" x="450" y="378" text-anchor="middle">reads text, writes text, runs no code</text>
<!-- The request -->
<rect class="sk-box" x="10" y="150" width="165" height="110" rx="10"/>
<text class="sk-label" x="24" y="174">Chat request</text>
<text class="tc-code" x="24" y="194">Is checkout slow?</text>
<rect class="tc-def" x="22" y="206" width="141" height="42" rx="6"/>
<text class="sk-label" x="32" y="224">Tool definition</text>
<text class="tc-code" x="32" y="240">countErrors</text>
<path class="sk-line" d="M34,260 L34,322 M34,284 L46,284 M34,303 L46,303 M34,322 L46,322"/>
<text class="sk-sub" x="52" y="288">name</text>
<text class="sk-sub" x="52" y="307">description</text>
<text class="sk-sub" x="52" y="326">input schema</text>
<!-- The response -->
<rect class="sk-box" x="730" y="166" width="160" height="78" rx="10"/>
<text class="sk-label" x="744" y="192">Chat response</text>
<text class="sk-sub" x="744" y="214">checkout has 412</text>
<text class="sk-sub" x="744" y="230">error events</text>
<!-- 1: request to model -->
<path class="tc-arrow" d="M175,205 L260,205 L260,326" marker-end="url(#tc-head)"/>
<!-- inside the model: reads the request, decides -->
<path class="tc-dot" d="M260,334 L260,344 L390,344 L390,334"/>
<!-- 2: tool call up to the harness -->
<path class="tc-arrow" d="M390,330 L390,248" marker-end="url(#tc-head)"/>
<!-- 3: run the tool -->
<path class="tc-arrow" d="M390,176 L390,76" marker-end="url(#tc-head)"/>
<!-- 4: result back -->
<path class="tc-arrow" d="M510,72 L510,172" marker-end="url(#tc-head)"/>
<!-- 5: result to the model -->
<path class="tc-arrow" d="M510,244 L510,326" marker-end="url(#tc-head)"/>
<path class="tc-dot" d="M510,334 L510,344 L640,344 L640,334"/>
<!-- 6: final answer -->
<path class="tc-arrow" d="M640,330 L640,205 L726,205" marker-end="url(#tc-head)"/>
<text class="tc-edge" x="268" y="300">question + tool</text>
<text class="tc-edge" x="398" y="300">tool call</text>
<text class="tc-edge" x="398" y="110">run</text>
<text class="tc-edge" x="518" y="110">412</text>
<text class="tc-edge" x="518" y="300">tool result</text>
<text class="tc-edge" x="648" y="300">answer</text>
<circle class="tc-step" cx="215" cy="186" r="10"/><text class="tc-step-n" x="215" y="190">1</text>
<circle class="tc-step" cx="372" cy="270" r="10"/><text class="tc-step-n" x="372" y="274">2</text>
<circle class="tc-step" cx="372" cy="98" r="10"/><text class="tc-step-n" x="372" y="102">3</text>
<circle class="tc-step" cx="528" cy="140" r="10"/><text class="tc-step-n" x="528" y="144">4</text>
<circle class="tc-step" cx="528" cy="270" r="10"/><text class="tc-step-n" x="528" y="274">5</text>
<circle class="tc-step" cx="685" cy="186" r="10"/><text class="tc-step-n" x="685" y="190">6</text>
</svg>
<figcaption>Figure 1.2. Tool calling in six steps. The model asks. The harness runs the tool. Redrawn from the Spring AI reference, <a href="https://docs.spring.io/spring-ai/reference/concepts.html">AI Concepts</a>, for the Log Incident Watcher.</figcaption>
</figure>

The numbers in Figure 1.2 match these steps. Table 1.1 maps each one to a harness job.

1. The request carries each tool definition: a name, a description, and an input schema.
2. The model replies with a tool call: the tool name and the arguments.
3. The harness finds the tool by name and runs it with those arguments.
4. The tool returns its result to the harness.
5. The harness sends the result back to the model.
6. The model writes the final answer from the result.

| Step | Harness job |
|---|---|
| 1 | Job 1: send the prompt and the tool list |
| 2 | Job 2: read the reply |
| 3 and 4 | Job 3: run the tool |
| 5 | Job 4: return the tool result |
| 6 | Job 5: no tool call in the reply, so stop |

<p class="caption">Table 1.1. Spring AI's six tool calling steps, mapped to the five harness jobs.</p>

- **The model never runs code.** Your app runs every tool.
- **Figure 1.2 shows one tool call.** A real run can repeat steps 2 to 5. Job 5 decides when to stop. Chapter 6 adds limits to that decision.
- **Spring AI can do steps 3 to 5 for you.** Chapter 4 uses that. Chapter 5 does them by hand.

**Summary:** A model only writes text. The harness sends the request, runs the tools, and decides when to stop.
