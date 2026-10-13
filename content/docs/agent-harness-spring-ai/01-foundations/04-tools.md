---
title: "Chapter 4: Tools"
linktitle: "4. Tools"
summary: "A tool is a Java method. The model chooses it from its name and description alone."
weight: 50

date: "2026-10-10T00:00:00Z"
toc: true
---

A tool is a Java method. The model chooses tools using only their names and descriptions. A vague description causes wrong choices.

```java
@Component
public class LogTools {

    @Tool(description = "Count error log events for one service in the last N minutes. Use this to check for a current error spike.")
    public int countErrors(
            @ToolParam(description = "Service name, for example checkout") String service,
            @ToolParam(description = "Look-back window in minutes, from 1 to 1440") int minutes) {
        return "checkout".equals(service) ? 412 : 3; // fake data
    }
}
```

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

Attach the tool with `.tools(logTools)` on the prompt. Exercise: rename the tool, then remove its description. Compare the model's choices each time.
