---
tags: [AI>prompt]
info: aberto.
date: 2025-02-10
type: post
layout: post
published: true
slug: copilot-agent-batch
title: 'Copilot Agent [batch]'
---
{% codeblock %}

User’s initial description of the task details:
~~~
PLACEHOLDER
~~~

We are performing an AI-driven development workflow with four key steps:
"""
• STEP 1: Brainstorm → Inquire about task details, remove ambiguity, explore edge cases, and attach references.
• STEP 2: Plan → Document code behavior, identify success criteria, refine specifications, create a file-specific plan, and prepare dependencies.
• STEP 3: Implement → Update and generate code, preserve coding conventions, track changes in a diff-friendly format, and integrate suggestions.
• STEP 4: Build, Test, and Repair → Build and test the code, detect errors or warnings, propose automated fixes, and refine.
"""

Now, please perform the first key step, as follows:
```
**STEP 1: Brainstorm** 
'''
• Inquire about the user’s initial description of the task  
• Gather and confirm requirements, constraints, and technical context
• Identify assumptions, distant edge cases, and success criteria
• Resolve ambiguities by asking targeted questions
• Help users attach relevant references to the task  
• Incorporate discovered details into the overall specification
'''
The goal here is to eliminate ambiguity and uncover hidden requirements. By posing targeted questions, you gain a deeper understanding of objectives and potential edge cases. This ensures you’re tackling the right problem and sets a strong foundation for subsequent steps.
```

:::

Now, please perform the second key step, as follows:
```
**STEP 2: Plan**
'''
• Explain current code behavior and usage  
• Identify success criteria for the task  
• Determine essential code context from repository content  
• Prepare bullet points of required functionalities or changes  
• Refine them based on user corrections or feedback
• Translate clarified requirements into precise specifications
• Translate specifications into a extensive, file-specific plan  
• Create file-by-file objectives: specify additions, modifications, deletions
• Outline an execution roadmap with dependency order
• Document coding conventions (e.g., ESLint, Prettier, Flake8) and tools
• Confirm feasibility
• Provide iterative plan revision via natural language prompts
'''
Building on the clarified specifications from Brainstorming, define a roadmap identifying the files and sections to modify, create, rename, or delete. The Plan STEP includes a thorough rationale behind these changes, ensuring each item is aligned with your ultimate goals. This step helps you handle project complexity by presenting a well-structured blueprint.
``` 

:::

Now, please perform the third key step, as follows:
```
**STEP 3: Implement**
'''
• Generate new or updated code for each file according to the plan
• Maintain consistent style, naming, and architecture
• Perform direct editing for adjustments
• Include robust error handling and logging frameworks where relevant
• Implement each and every copilot suggestions
• Provide a clear diff or changelog for reviews and integrations
'''
Use the comprehensive plan to apply specific modifications in the codebase. Follow the repository’s coding guidelines and any custom instructions to maintain consistency and code quality. “Production-ready” code in this context means ensuring each file is updated appropriately, variables and functions are well-named, and logic changes adhere to desired standards. If needed, incorporate short tests or inline validations to confirm immediate functionality, setting the stage for a full build or test process.
```

:::

Now, please perform the last key step, as follows:
```
**STEP 4: Build, Test, and Repair**
'''
• Offer integrated build and test commands  
• Execute build commands (e.g., “npm run build”, “docker build”)
• Run unit, integration, and coverage tests (e.g., “npm test”, “pytest”)
• Check for lint errors, static analysis warnings, and security vulnerabilities
• Repair discovered issues or roll back to earlier steps as needed to update plan or code to address repeated errors  
• Finalize once code passes validation checks
'''
Finally, validate your solution by building and running tests against the updated codebase. Linting, static analysis, and continuous integration checks can help uncover issues before integration. If failures or warnings arise, refine your approach—either revisiting the Plan or using the Brainstorming process again for deeper exploration. This cyclical feedback loop ensures a stable, high-quality solution.
```

NOTES:
• At each step, validate completion before moving on
• Return to earlier steps if major changes or corrections are necessary
• Use CI/CD pipelines (GitHub Actions, Jenkins, etc.) to automate testing and deployment
• Emphasize continuous improvement and iterative refinement at every step
• All key steps can be repeated or refined as needed until the task is complete and validated

{% endcodeblock %}
