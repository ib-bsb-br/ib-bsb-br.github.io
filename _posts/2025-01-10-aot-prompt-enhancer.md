---
tags: AI>prompt
info: aberto.
date: 2025-01-10
type: post
layout: post
published: true
slug: aot-prompt-enhancer
title: 'AoT prompt enhancer'
---
{% codeblock %}
**Task Overview:**

You are assigned to enhance and restructure a given user prompt by applying the **Algorithm of Thoughts (AoT)** framework. This involves breaking down the original prompt into its fundamental components and then reconstructing it into a coherent, well-organized prompt that adheres to the AoT methodology.

**Objectives:**

1. **Decompose the Original Prompt:** Dissect the provided prompt into distinct sections based on the `AoT Prompt Framework`.
2. **Reassemble into a Cohesive Prompt:** Combine the separated sections into a unified and comprehensive final prompt.

**Instructions:**

1. **Transform into Disjoint Components:**

   Carefully analyze the original prompt and separate it into the following AoT framework sections:

   - **Problem Statement:** Clearly define the main issue or topic addressed in the prompt.
   - **Background Information:** Include any relevant context or details that support the understanding of the problem.
   - **Gather Information:** Direct the Language Model (LLM) to collect essential data or insights related to the problem.
   - **Analyze the Information:** Guide the LLM to examine patterns, relationships, or anomalies within the gathered data.
   - **Formulate a Hypothesis:** Encourage the LLM to develop a preliminary solution or theoretical explanation based on the analysis.
   - **Test the Hypothesis:** Instruct the LLM to propose methods for validating or challenging the initial hypothesis.
   - **Draw Conclusions:** Ask the LLM to summarize the findings and present a refined solution or answer.
   - **Reflect:** Prompt the LLM to consider broader implications, potential next steps, or additional questions arising from the conclusions.

   *Example Transformation:*

   ```AoT_Prompt_Framework
   Problem Statement: [Define the core issue from the original prompt]
   
   Background Information: [Add necessary context or details]
   
   Gather Information: [Instruct the LLM to collect relevant data]
   
   Analyze the Information: [Guide the LLM to examine the collected data]
   
   Formulate a Hypothesis: [Encourage the LLM to propose a preliminary solution]
   
   Test the Hypothesis: [Instruct the LLM to validate or challenge the hypothesis]
   
   Draw Conclusions: [Summarize findings and provide a refined solution]
   
   Reflect: [Consider broader implications and next steps]
   
   Final Prompt: <--! placeholder -->
   ```

2. **Reconstruct into Final Prompt:**

   - **Integrate Sections:** Combine the separated sections into a seamless and logically flowing final prompt.
   - **Ensure Clarity:** Make sure the final prompt is clear, actionable, and aligns with the AoT framework.
   - **Maintain Structure:** Preserve the integrity of each AoT component to facilitate a step-by-step reasoning process for the LLM.

**Desired Outcome:**

A meticulously structured final prompt that incorporates all elements of the AoT framework, enabling the Language Model to engage in a methodical reasoning process and generate precise, insightful responses.

**Response Specifications:**

- **Format:** Utilize the `AoT_Prompt_Framework` structure with clearly defined sections.
- **Length:** Ensure each section is concise yet comprehensive, avoiding unnecessary verbosity.
- **Clarity:** Employ precise and unambiguous language to facilitate easy understanding and effective guidance for the LLM.

**Example Output 1:**

```AoT_Prompt_Framework_1
Problem Statement: [Define the core issue from the original prompt]

Background Information: [Add necessary context or details]

Gather Information: [Instruct the LLM to collect relevant data]

Analyze the Information: [Guide the LLM to examine the collected data]

Formulate a Hypothesis: [Encourage the LLM to propose a preliminary solution]

Test the Hypothesis: [Instruct the LLM to validate or challenge the hypothesis]

Draw Conclusions: [Summarize findings and provide a refined solution]

Reflect: [Consider broader implications and next steps]

Final Prompt: <--! placeholder -->
```

**Example Output 2:**
"""
**Original Prompt:**

*"Discuss the benefits of exercise."*

**Enhanced Prompt Using the AoT Framework:**

```AoT_Prompt_Framework
Problem Statement: Analyze and explain the various benefits of regular physical exercise on human health and well-being.

Background Information: Regular physical exercise is known to have significant impacts on physical fitness, mental health, and overall quality of life.

Gather Information: Collect data on the physical, mental, and emotional benefits of exercise from reputable sources such as medical journals, health organizations, and scientific studies.

Analyze the Information: Examine how different forms of exercise contribute to health improvements, identify patterns in the benefits reported, and consider various population groups.

Formulate a Hypothesis: Propose that engaging in regular physical activity leads to comprehensive health benefits that affect multiple aspects of an individual's life.

Test the Hypothesis: Explore case studies, statistical data, and expert opinions that support or refute the proposed hypothesis.

Draw Conclusions: Summarize the findings to confirm the hypothesis, highlighting the key benefits of exercise and any limitations or considerations.

Reflect: Consider the broader implications for public health initiatives, personal lifestyle choices, and future research on exercise science.

Final Prompt: Compose a detailed essay that discusses the physical, mental, and emotional benefits of regular exercise, supported by scientific evidence, and reflects on its significance for individuals and society.

```
"""

---

**Input Prompt:**

~~~
*Please insert the original prompt here.*
~~~

**Guidelines:**

- **Step-by-Step Reasoning:** Adopt a systematic approach, ensuring each stage of the AoT framework is thoroughly addressed.
- **Positive Instructions:** Focus on clear directives about the actions to take, fostering a constructive process.
- **Avoid Ambiguity:** Use explicit instructions to eliminate any potential for misinterpretation.
- **Adaptability:** While following the AoT framework, allow flexibility to accommodate different types of prompts or contexts.

**Final Note:**

Ensure that the enhanced prompt aligns seamlessly with the user's initial intention, providing a robust foundation for the Language Model to generate effective and insightful responses.

---
{% endcodeblock %}