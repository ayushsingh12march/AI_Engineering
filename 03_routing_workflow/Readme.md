# Routing Workflow Example

This example demonstrates the implementation of a routing workflow using LangGraph, following the principles outlined in [Anthropic's guide on building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

## Overview

Routing is a workflow pattern that classifies input and directs it to specialized followup tasks. This pattern allows for separation of concerns and enables building specialized prompts for different types of content generation.

## Implementation Details

Our example implements a content generation router with the following components:

1. **Structured Output for Routing**
   - Uses Pydantic model (`Route`) to define possible routing paths
   - Supports three content types: poems, stories, and jokes
   - Ensures type-safe routing decisions

2. **Specialized Writers**
   - `poem_writer`: Generates poetic content
   - `story_writer`: Creates narrative content
   - `joke_writer`: Produces humorous content
   - Each writer is optimized for its specific content type

3. **Router Function**
   - Uses structured output LLM to make routing decisions
   - Analyzes user input to determine the most appropriate content type
   - Makes decisions based on input context and requirements

4. **Workflow Graph**
   - Built using LangGraph's StateGraph
   - Implements conditional routing based on LLM decisions
   - Maintains clear separation between routing logic and content generation

## When to Use This Pattern

According to Anthropic's guidelines, routing workflows are ideal when:
- Tasks have distinct categories that require different handling
- Classification can be done accurately by an LLM
- Optimizing for one type of input might hurt performance on others
- You need to maintain specialized prompts for different tasks

## Benefits

1. **Improved Quality**
   - Each writer specializes in one type of content
   - Better results through focused prompts
   - Clear separation of concerns

2. **Flexibility**
   - Easy to add new content types
   - Simple to modify routing logic
   - Maintainable specialized prompts

3. **Scalability**
   - Can route to different model sizes based on task complexity
   - Easy to add new routing paths
   - Supports growing content types

## Usage

```python
# Initialize and compile the workflow
router_workflow = router_builder.compile()

# View the workflow graph
print(router_workflow.get_graph().draw_mermaid())

# Run with input
state = router_workflow.invoke({
    "input": "Write me a poem about stock market and life of a software engineer"
})
print(state)
```

## Dependencies

- langgraph
- Python 3.10+
- Claude 3 Sonnet (via custom client)
- pydantic for structured output

## Best Practices

1. **Clear Routing Logic**
   - Use structured output for routing decisions
   - Implement clear routing conditions
   - Document routing paths

2. **Specialized Writers**
   - Keep writers focused on single content types
   - Optimize prompts for each type
   - Maintain consistent output formats

3. **Error Handling**
   - Handle edge cases gracefully
   - Provide fallback paths
   - Validate routing decisions

## Example Use Cases

1. **Content Generation**
   - Route to different content types (poems, stories, jokes)
   - Each type handled by specialized writer
   - Maintains quality through focus

2. **Customer Support**
   - Route queries to appropriate departments
   - Handle different request types differently
   - Optimize response strategies

3. **Model Selection**
   - Route simple tasks to smaller models
   - Complex tasks to more capable models
   - Optimize cost and performance

## References

- [Building Effective Agents - Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-effective-agents)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
