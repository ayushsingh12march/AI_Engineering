# Evaluator-Optimizer Workflow Example

This directory demonstrates the Evaluator-Optimizer workflow pattern, following best practices from [Anthropic's guide on building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

## Overview

The Evaluator-Optimizer workflow is a powerful pattern where one LLM generates content while another provides evaluation and feedback in a loop. This creates an iterative refinement process that can significantly improve output quality.

In this example, we implement a joke-writing system where:
1. One LLM writes jokes on given topics
2. Another LLM evaluates the jokes and provides feedback
3. The system iterates to improve jokes based on feedback

## Key Components

### 1. Joke Writer
- Takes a topic and generates a joke
- Can incorporate feedback from previous iterations
- Maintains a retry counter to limit iterations

### 2. Evaluator
- Grades jokes as "funny" or "not_funny"
- Provides structured feedback for improvement
- Uses Pydantic models for consistent output format

### 3. Workflow Control
- Manages the iteration loop between writer and evaluator
- Implements conditional logic for joke refinement
- Limits maximum retries to prevent infinite loops

## Implementation Details

The workflow is implemented using LangGraph and consists of:

1. **State Management**
   - Tracks topic, current joke, evaluation results, and retry count
   - Uses TypedDict for type-safe state handling

2. **Structured Evaluation**
   - Uses Pydantic models for structured feedback
   - Ensures consistent evaluation format
   - Provides clear improvement suggestions

3. **Conditional Flow**
   - Decides whether to rewrite jokes based on:
     - Current evaluation grade
     - Number of retries attempted
   - Terminates after success or max retries

## Usage

The workflow is demonstrated in `langraph_evaluator_optimizer.py`. To use:

```python
# Create and invoke the workflow
state = evaluator_optimizer_workflow.invoke({"topic": "indian cricket team"})
print(state)
```

## Best Practices

1. **Clear Evaluation Criteria**
   - Define specific success metrics
   - Use structured output for consistent evaluation
   - Provide actionable feedback

2. **Controlled Iteration**
   - Set appropriate retry limits
   - Include clear termination conditions
   - Monitor performance across iterations

3. **Effective Feedback Loop**
   - Ensure feedback is specific and actionable
   - Maintain context across iterations
   - Track improvement progress

## Dependencies

- Python 3.10+
- LangGraph for workflow orchestration
- Pydantic for structured data handling
- Claude 3 Sonnet for LLM capabilities

## Getting Started

1. Ensure you have Python 3.10+ installed
2. Set up a virtual environment
3. Install requirements from requirements.txt
4. Review the example in `langraph_evaluator_optimizer.py`
5. Run the example to see the workflow in action

## When to Use This Pattern

The Evaluator-Optimizer workflow is particularly effective when:
- You have clear evaluation criteria
- Iterative refinement provides measurable value
- LLM feedback can meaningfully improve outputs
- Quality is more important than latency

## References

- [Building Effective Agents - Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-effective-agents)
