# Augmented LLM Examples

This directory demonstrates different ways to augment Large Language Models (LLMs) with additional capabilities, following best practices from [Anthropic's guide on building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

## Overview

The examples show how to enhance LLMs with various augmentations that improve their capabilities while maintaining simplicity and composability. We demonstrate three key augmentation patterns:

1. Structured Output
2. Tool Calling
3. Memory Management

## Examples

### 1. Structured Output Augmentation

Shows how to make LLMs output in specific structured formats using Pydantic models. This is useful for:
- Ensuring consistent output format
- Input validation
- Easy parsing and processing of LLM responses

Example: `SearchQuery` model that structures web search queries with justification.

### 2. Tool Calling Augmentation

Demonstrates how to give LLMs access to external tools and functions. Benefits include:
- Extending LLM capabilities with custom functions
- Controlled access to external systems
- Verifiable and testable outputs

Example: Simple multiplication tool that shows the basic pattern of tool integration.

### 3. Memory Augmentation

Implements a simple but effective conversation memory system that allows the LLM to:
- Maintain context across multiple interactions
- Reference previous conversations
- Build more coherent and contextual responses

Example: Conversation memory that remembers user information and can reference it in later interactions.


## Usage

Each augmentation type is demonstrated in `langraph_augmented_llm.py`. The examples show:
- How to set up each augmentation
- Basic usage patterns
- Example outputs and interactions

## Best Practices

1. Start with the simplest solution possible
2. Add complexity only when demonstrably needed
3. Focus on clear tool documentation and interfaces
4. Test thoroughly in sandboxed environments
5. Implement appropriate guardrails for production use

## Dependencies

- Python 3.10+
- Pydantic for structured data handling
- Claude 3 Sonnet for LLM capabilities

## Getting Started

1. Ensure you have Python 3.10+ installed
2. Set up a virtual environment
3. Install requirements from requirements.txt
4. Review the examples in `langraph_augmented_llm.py`
5. Run the examples to see augmentations in action

## References

- [Building Effective Agents - Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-effective-agents)
