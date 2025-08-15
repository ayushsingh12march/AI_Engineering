# Orchestrator-Worker Workflow Example

This example demonstrates the implementation of an orchestrator-worker workflow using LangGraph, following the principles outlined in [Anthropic's guide on building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

## Overview

The orchestrator-worker workflow is a pattern where a central LLM (the orchestrator) dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results. This pattern is particularly powerful for complex tasks where subtasks can't be predetermined and need to be dynamically identified based on the input.

## Implementation Details

Our example implements a report generation system with the following components:

1. **Orchestrator**
   - Analyzes the report topic
   - Generates a structured plan with sections
   - Delegates sections to workers
   - Manages overall workflow

2. **Workers**
   - Specialized LLMs for writing report sections
   - Each worker focuses on one section
   - Work in parallel for efficiency
   - Generate content based on section requirements

3. **Synthesizer**
   - Combines worker outputs
   - Creates coherent final report
   - Maintains structure and flow
   - Ensures consistency

4. **State Management**
   - Uses TypedDict for type safety
   - Tracks overall report state
   - Manages worker states independently
   - Handles parallel accumulation of results

## When to Use This Pattern

According to Anthropic's guidelines, the orchestrator-worker pattern is ideal when:
- Tasks require dynamic breakdown into subtasks
- The number and nature of subtasks depend on the input
- Complex coordination between multiple components is needed
- Tasks benefit from specialized worker focus

## Benefits

1. **Flexibility**
   - Dynamic task decomposition
   - Adaptive to input complexity
   - Scalable worker allocation
   - Flexible synthesis strategies

2. **Efficiency**
   - Parallel task execution
   - Specialized worker focus
   - Optimized resource usage
   - Reduced overall latency

3. **Quality**
   - Expert handling of subtasks
   - Comprehensive coverage
   - Coordinated output synthesis
   - Maintained consistency

## Usage

```python
# Initialize and compile the workflow
orchestrator_worker_workflow = orchestrator_worker_builder.compile()

# View the workflow graph
print(orchestrator_worker_workflow.get_graph().draw_mermaid())

# Run with a topic
state = orchestrator_worker_workflow.invoke({
    "topic": "Create a report on Agentic RAG vs ReRanker RAG"
})
print(state)
```

## Dependencies

- langgraph
- Python 3.10+
- Claude 3 Sonnet (via custom client)
- pydantic

## Best Practices

1. **Task Decomposition**
   - Clear section definitions
   - Logical task boundaries
   - Appropriate granularity
   - Independent worker tasks

2. **Worker Management**
   - Efficient parallel execution
   - Clear worker responsibilities
   - Proper state isolation
   - Error handling

3. **Result Synthesis**
   - Coherent combination strategy
   - Maintained structure
   - Preserved context
   - Quality validation

## Example Use Cases

1. **Report Generation**
   - Complex document creation
   - Multi-section reports
   - Research summaries
   - Technical documentation

2. **Code Generation**
   - Multi-file changes
   - Complex refactoring
   - System architecture
   - Code review automation

3. **Research Tasks**
   - Information gathering
   - Multi-source analysis
   - Comprehensive summaries
   - Structured findings

## Advanced Applications

1. **Adaptive Systems**
   - Dynamic worker allocation
   - Load balancing
   - Resource optimization
   - Quality-based routing

2. **Complex Workflows**
   - Multi-stage processing
   - Conditional execution
   - Iterative refinement
   - Quality assurance

## References

- [Building Effective Agents - Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-effective-agents)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
