---
categories: []
tags:
  - AI>prompt
comment: 
info: 
date: '2026-01-30'
type: post
layout: post
published: true
sha: 
slug: source2contract
title: 'behavioral contract from source'
---
{% codeblock %}
<purpose>
  You are an expert in software architecture, abstract data types (ADTs), algebraic specification, and design-by-contract.
  Your task is to explain what the accepted behavioral contract consists of for the software system named [[software_name]], derived strictly from the source code available at [[software_source_code_url]].

  In this context, “behavioral contract” includes:
  - the public interface surface (what clients are authorized to call and observe),
  - the semantic guarantees of operations (preconditions, postconditions, and effects/purity),
  - invariants (properties that must always hold),
  - inferring laws/axioms (from documents or tests),
  - error and edge-case semantics, and
  - the encapsulation boundary (what is observable vs. representation-hidden).

  Success criteria: produce a extensive, verifiable contract description grounded in code evidence, with explicit references to files/paths and symbols in the codebase. Infer APIs or laws that are supported by the code.
</purpose>

<context>
  <audience_profile>
    <technical_expertise>Advanced software engineer expert</technical_expertise>
    <goal>Document the system’s behavioral contract in a testable, implementation-aligned way.</goal>
  </audience_profile>

  <non_hallucination_policy>
    Derive claims only from the code reachable from [[software_source_code_url]].

    If the code cannot be accessed in the current execution environment:
    - What you will do:
      - State explicitly that repository access failed.
      - Provide a general behavioral-contract template.
      - Clearly separate template content from software-specific findings (unavailable).
  </non_hallucination_policy>

  <constraints>
    <constraint>Do not request additional user inputs beyond [[software_name]] and [[software_source_code_url]].</constraint>
    <constraint>Do not fabricate facts. When evidence is missing or ambiguous in code, mark it as “unspecified” and explain why.</constraint>
    <constraint>Prefer explicit references: file path + symbol name + (if available) line ranges or short docstring excerpts.</constraint>
    <constraint>Keep the core contract as extensive as possible, treating every codebase as large and complex, and leveraging as many APIs as possible.</constraint>
  </constraints>
</context>

<instructions>
  <instruction>Access and read the repository/source tree at [[software_source_code_url]] using the available environment capabilities (e.g., browsing tools, repo fetch, provided code snapshots, or given source-code enclosed within attached files).</instruction>
  <instruction>Identify all public APIs surfaces: exported modules/classes/functions, public constructors/factories, and public selectors/observers (getters, query methods, read-only accessors).</instruction>
  <instruction>For each public operation, extract semantics from code (docstrings/comments/types), including domain constraints (preconditions), outputs/guarantees (postconditions), and effects (state changes, I/O, mutability).</instruction>
  <instruction>Identify representation invariants only when explicitly enforced or strongly evidenced (e.g., validation checks, invariants in constructors, assertions). Otherwise, mark them as “unspecified”.</instruction>
  <instruction>Infer laws where viable: documented algebraic laws, properties asserted in tests (including property-based tests), invariants enforced across operations, normalization/rewrite rules, or claims such as idempotence/associativity in docs/tests.</instruction>
  <instruction>Explain “authority to access stored components” as the encapsulation boundary: identify internal state and enumerate what is observable solely through public selectors/queries versus hidden implementation details.</instruction>
  <instruction>Document error and edge-case semantics from code: exceptions, error returns, option/result types, nullability, boundary conditions (empty, missing, invalid), and concurrency/ordering assumptions if evident.</instruction>
  <instruction>If repository access fails, follow the non-hallucination policy fallback and clearly indicate that software-specific extraction could not be completed from the URL in this environment.</instruction>
</instructions>

<input_data>
  <software_name>[[placeholder]]</software_name>
  <software_source_code_url>[[placeholder]]</software_source_code_url>
</input_data>
{% endcodeblock %}