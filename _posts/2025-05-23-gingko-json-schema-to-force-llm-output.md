---
tags: [scratchpad]
info: aberto.
date: 2025-05-23
type: post
layout: post
published: true
slug: gingko-json-schema-to-force-llm-output
title: 'Gingko JSON Schema to force LLM output'
---
{% codeblock json %}
{
    "name": "gingko",
    "strict": false,
    "schema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "The main idea or concept of the AI assistant's response."
            },
            "children": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "A sub-idea or element related to the parent's content."
                        },
                        "children": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "content": {
                                        "type": "string",
                                        "description": "A further sub-idea or element related to the parent's content."
                                    },
                                    "children": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "content": {
                                                    "type": "string",
                                                    "description": "An additional sub-idea or element at a deeper level."
                                                },
                                                "children": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "content": {
                                                                "type": "string",
                                                                "description": "A more deeply nested sub-idea or element."
                                                            },
                                                            "children": {
                                                                "type": "array",
                                                                "items": {
                                                                    "type": "object",
                                                                    "properties": {
                                                                        "content": {
                                                                            "type": "string",
                                                                            "description": "The deepest sub-idea or element."
                                                                        },
                                                                        "children": {
                                                                            "type": "array",
                                                                            "items": {
                                                                                "type": "object",
                                                                                "properties": {
                                                                                    "content": {
                                                                                        "type": "string",
                                                                                        "description": "An even deeper sub-idea or element."
                                                                                    },
                                                                                    "children": {
                                                                                        "type": "array",
                                                                                        "items": {
                                                                                            "$ref": "#"
                                                                                        }
                                                                                    }
                                                                                },
                                                                                "required": [
                                                                                    "content",
                                                                                    "children"
                                                                                ]
                                                                            }
                                                                        }
                                                                    },
                                                                    "required": [
                                                                        "content",
                                                                        "children"
                                                                    ]
                                                                }
                                                            }
                                                        },
                                                        "required": [
                                                            "content",
                                                            "children"
                                                        ]
                                                    }
                                                }
                                            },
                                            "required": [
                                                "content",
                                                "children"
                                            ]
                                        }
                                    }
                                },
                                "required": [
                                    "content",
                                    "children"
                                ]
                            }
                        }
                    },
                    "required": [
                        "content",
                        "children"
                    ]
                }
            }
        },
        "required": [
            "content",
            "children"
        ]
    }
}
{% endcodeblock %}