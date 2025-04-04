---

tags: [AI>prompt]
info: aberto.
date: 2024-10-26
type: post
layout: post
published: true
slug: simon-says-documentation
title: 'Simon says: Documentation'
---
{% codeblock markdown %}
**Task Overview:**

You are required to analyze and organize unstructured project data to create comprehensive and effective documentation that ensures project and task maintainability. The goal is to transform the provided unstructured data into well-organized, detailed documentation that can be easily understood and used for future reference, even after significant downtime or by third parties unfamiliar with the project.

---

**Instructions:**

Please follow the steps below carefully to analyze and organize the data:

---

**1. Data Review and Key Elements Identification:**

   - **Thoroughly review** the unstructured project data provided.
   - **Identify and extract** key elements that need documentation, such as:
     - **Background** information of the project.
     - **Current state** and progress of the project.
     - **Relevant resources** and references.
     - **Design considerations** and decision-making processes.
     - **Screenshots or demos** illustrating features or issues.
     - **Timestamps** of significant events or changes.
     - **Implementation details** including code snippets or algorithms.
     - **Testing information** and results.
     - **Documentation updates** and version history.
     - **Causality chain** explaining the reasoning behind information (What does the information consist of? Why is it important?).

---

**2. Application of Documentation Principles:**

   - **Apply the following core documentation principles** to each piece of extracted information:
     - **Causality Chain Initiation:** Ensure every change or piece of information originates from a clear causality chain.
     - **Contextual Documentation:** Recognize that documentation must be relevant to its context within the project.
     - **Validation Through Testing:** Validate information through appropriate testing procedures.
     - **Integration of Implementation and Testing:** Include both implementation details and testing results in the final documentation.

---

**3. Organization of Information:**

   - **Document All Details:** Record all relevant information to eliminate reliance on memory.
   - **Structure Projects with Tests First:** Begin documentation with testing procedures and results.
   - **Link Back to Causality:** Ensure all documentation connects back to the original issues and their causality.
   - **Prepare for Third-Party Maintenance:** Organize documentation with the assumption that third parties will maintain the project.
   - **Use Unit Tests for Documentation Coverage:** Implement unit tests to verify that documentation is complete and accurate.
   - **Maintain Deployability:** Ensure that the documentation supports the project's ability to be deployed smoothly.
   - **Focus on Actual Implementations:** Document what has been built and implemented, rather than theoretical plans.

---

**4. Implementation of Recommendations:**

   - **Incorporate the following recommendations** to enhance documentation and project maintainability:
     - **Effective Structuring of Issue Documentation**
     - **Creation and Maintenance of Comprehensive Documentation**
     - **Ensuring Permanency and Scalability in Documentation**
     - **Implementation of Documentation Unit Tests**
     - **Horizontal Scaling of Project Management through Efficient Documentation**

---

**5. Creation of a Detailed Paper Trail:**

   - **Maintain an extensive record** of all decisions and changes made during this process.
   - **Justify each decision** based on the provided data.
   - **Ensure traceability** so that anyone can understand the reasoning behind each decision.

---

**Output Format:**

Present your findings and organized documentation in the following structured format:

```markdown
<analysis>
1. **Initial Data Review:**
   - [Provide extensive documentation of key points extracted from the unstructured data.]

2. **Identification of Elements:**
   - [List each key element to be documented, numbered sequentially.]

3. **Application of Documentation Principles:**
   - [Explain how each piece of information aligns with the core documentation principles.]

4. **Organization Process:**
   - [Outline the step-by-step approach taken to categorize and structure the information.]

5. **Implementation of Recommendations:**
   - [Detail how each recommendation was implemented based on the analyzed data and its impact on project maintainability.]
</analysis>

<organized_information>
<data>
[Provide a detailed list of the organized data.]
</data>

<documentation>
[Present the final documentation entries, thoroughly detailing each aspect without placeholders or unnecessary commentary.]
</documentation>
</organized_information>

<paper_trail>
[Include a clear and extensive record of decisions and changes made, justifying each based on the provided data.]
</paper_trail>
```

---

**Example:**

*Note: This example uses placeholder data to illustrate the expected output format.*

```markdown
<analysis>
1. **Initial Data Review:**
   - The project currently lacks centralized documentation.
   - Recent code updates have introduced new features not documented.
   - Testing procedures are inconsistent and not fully recorded.

2. **Identification of Elements:**
   1. Centralized documentation system establishment.
   2. Documentation of new features added.
   3. Standardization of testing procedures.
   4. Implementation details of recent updates.
   5. Background context for project decisions.

3. **Application of Documentation Principles:**
   - **Causality Chain Initiation:** Identified missing documentation leading to confusion and errors.
   - **Contextual Documentation:** Ensured new features are documented within the context of the overall system.
   - **Validation Through Testing:** Standardized procedures to validate new implementations.
   - **Integration of Implementation and Testing:** Linked code updates directly with testing results.

4. **Organization Process:**
   - Created a centralized documentation repository.
   - Developed templates for feature documentation and testing results.
   - Categorized information based on functionality and relevance.
   - Linked all documentation entries back to specific changes or updates.

5. **Implementation of Recommendations:**
   - **Effective Structuring:** Organized documents by modules and features.
   - **Comprehensive Documentation:** Included detailed descriptions, code snippets, and test results.
   - **Permanency and Scalability:** Set up version control for documentation updates.
   - **Documentation Unit Tests:** Implemented checks to ensure documentation is updated with each code commit.
   - **Horizontal Scaling:** Documented procedures to onboard new team members efficiently.
</analysis>

<organized_information>
<data>
- Established `/docs` directory for all documentation.
- Documented new features: Feature A, Feature B.
- Standardized testing procedures outlined in `/docs/testing.md`.
- Provided background context in `/docs/background.md`.
- Recorded implementation details in `/docs/implementation.md`.
</data>

<documentation>
- **Feature A Documentation:** Includes purpose, implementation details, usage examples, and test results.
- **Feature B Documentation:** Details integration with existing systems, potential issues, and verification steps.
- **Testing Procedures:** Step-by-step guide on executing and recording tests.
- **Background Context:** Explains project origins, objectives, and decision rationale.
- **Implementation Details:** Technical specifications, code architecture, and dependency management.
</documentation>
</organized_information>

<paper_trail>
- **Decision to Centralize Documentation:** Based on confusion from team members due to scattered information.
- **Creation of Documentation Templates:** To ensure consistency and completeness across all documents.
- **Standardization of Testing Procedures:** Aimed at improving reliability and validity of test results.
- **Linking Documentation to Code Commits:** For traceability and accountability.
- **Version Control Implementation:** To manage changes and updates systematically.
</paper_trail>
```

---

**Final Notes:**

- **Replace the placeholder data and examples** with information extracted from the provided unstructured project data.
- **Ensure thoroughness and clarity** in your final output, adhering closely to the specified format.
- The **analysis and organized documentation** should enable anyone to understand and maintain the project without prior knowledge.

---

**Unstructured Project Data:**

Please analyze the following unstructured project data:

~~~

~~~

{% endcodeblock %}
