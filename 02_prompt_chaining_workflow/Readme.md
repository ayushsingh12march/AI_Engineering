# Prompt Chaining Workflow Example

This example demonstrates the implementation of a prompt chaining workflow using LangGraph, following the principles outlined in [Anthropic's guide on building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

## Overview

Prompt chaining is a workflow pattern that decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one. The workflow includes programmatic checks ("gates") to ensure the process stays on track.

## Implementation Details

Our example implements a joke generation workflow with the following components:

1. **State Management**
   - Uses TypedDict to maintain state across steps
   - Tracks topic, original joke, improved joke, and polished joke

2. **Workflow Steps**
   - `generate_joke`: Creates initial joke about a given topic
   - `improve_joke`: Enhances the joke by mocking the punchline
   - `polish_joke`: Adds a surprising twist to the improved joke

3. **Gate Function**
   - `check_punchline`: Verifies if the joke has proper punctuation (? or !)
   - Routes to improvement if check fails, ends if passes

4. **Workflow Graph**
   - Built using LangGraph's StateGraph
   - Visualizable workflow with conditional paths
   - Clear state transitions and decision points

## When to Use This Pattern

According to Anthropic's guidelines, prompt chaining is ideal when:
- Tasks can be cleanly decomposed into fixed subtasks
- Trading latency for higher accuracy is acceptable
- Each step needs focused attention for better results

## Benefits

1. **Improved Quality**
   - Each step focuses on a specific aspect of joke creation
   - Gates ensure quality standards are met
   - Iterative improvement through multiple LLM calls

2. **Maintainability**
   - Clear separation of concerns
   - Easy to modify individual steps
   - Transparent workflow visualization

3. **Flexibility**
   - Easy to add new steps or checks
   - Configurable routing based on quality gates
   - Adaptable to different topics

## Usage

```python
# Initialize and run the workflow
chain = workflow.compile()

# View the workflow graph
print(chain.get_graph().draw_mermaid())

# Run with a topic
state = chain.invoke({"topic": "Software Engineers"})
print(state)
```

## Dependencies

- langgraph
- Python 3.10+
- Claude 3 Sonnet (via custom client)

## Best Practices

1. **Keep Steps Focused**
   - Each step should have a single, clear responsibility
   - Use descriptive names for steps and functions
   - Include documentation for each component

2. **Quality Gates**
   - Implement meaningful checks between steps
   - Use gates to ensure output quality
   - Provide clear failure paths

3. **State Management**
   - Use typed state definitions
   - Keep state updates clear and explicit
   - Track all necessary information between steps

## References

- [Building Effective Agents - Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-effective-agents)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
