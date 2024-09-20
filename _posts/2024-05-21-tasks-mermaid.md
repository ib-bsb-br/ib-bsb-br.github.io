---
title: Task Prioritization
date: 2024-05-21
tags: tasks
type: post
layout: post
---

{% mermaid %}
flowchart TD
    A[Start] --> B{Specific\ndeadline?}
    B -->|Yes| C{Delay causes\nharm?}
    B -->|No| D{Delay causes\nharm?}
    
    subgraph "Urgency & Time-Sensitivity"
        C -->|Yes| E[Urgent &\nTime-Sensitive]
        C -->|No| F[Not Urgent &\nTime-Sensitive]
        D -->|Yes| G[Urgent &\nNot Time-Sensitive]
        D -->|No| H[Not Urgent &\nNot Time-Sensitive]
    end
    
    E & F & G & H --> I{Multi-day\ntask?}
    
    subgraph "Task Duration & Final Categorization"
        I -->|Yes| J[Multi-Day]
        I -->|No| K[Single-Day]
        
        J --> L{Type?}
        K --> M{Type?}
        
        L -->|E| N[Schedule immediately,\nbreak into steps]
        L -->|F| O[Schedule,\nbreak into steps]
        L -->|G| P[Begin immediately,\nplan work]
        L -->|H| Q[Allocate time,\nwork gradually]
        
        M -->|E| R[Prioritize and\ncomplete today]
        M -->|F| S[Plan for\ndeadline day]
        M -->|G| T[Complete\nASAP today]
        M -->|H| U[Complete when\npossible]
    end
    
    N & O & P & Q & R & S & T & U --> V[End]
{% endmermaid %}
