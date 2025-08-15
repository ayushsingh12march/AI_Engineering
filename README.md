# 🤖 Building_Agents

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.0.19-orange)
![License](https://img.shields.io/badge/license-MIT-green)

**A comprehensive toolkit for building advanced AI agents using LangGraph**

[Key Features](#-key-features) •
[Installation](#-installation) •
[Quick Start](#-quick-start) •
[Workflows](#-workflows) •
[Contributing](#-contributing)

</div>

## 🌟 Key Features

- **6 Production-Ready Workflows**: From basic LLM augmentation to complex orchestrator-worker patterns
- **Best Practices**: Implements patterns from Anthropic's guide on building effective agents
- **Type Safety**: Leverages Python's type system for robust agent development
- **Modular Design**: Easy to understand, extend, and customize for your needs
- **Real-world Examples**: Each workflow comes with practical demonstrations

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Building_Agents.git
cd Building_Agents

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Quick Start

```python
from building_agents.evaluator_optimizer_workflow import evaluator_optimizer_workflow

# Try the evaluator-optimizer workflow
state = evaluator_optimizer_workflow.invoke({
    "topic": "artificial intelligence"
})
print(state)
```

## 📚 Workflows

1. **[Augmented LLM](01_augmented_llm/)** 
   - Basic LLM enhancement with additional capabilities
   - Perfect starting point for agent development

2. **[Prompt Chaining](02_prompt_chaining_workflow/)**
   - Sequential prompt execution and composition
   - Demonstrates effective prompt engineering

3. **[Routing](03_routing_workflow/)**
   - Dynamic task routing between different components
   - Intelligent workflow decision making

4. **[Parallel Processing](04_parallel_workflow/)**
   - Concurrent task execution for efficiency
   - Handles complex parallel workflows

5. **[Orchestrator-Worker](05_orchestrator_worker_workflow/)**
   - Advanced pattern for distributed task management
   - Scalable agent architecture

6. **[Evaluator-Optimizer](06_evaluator_optimizer_workflow/)**
   - Self-improving system with feedback loops
   - Implements iterative refinement

## 🛠️ Dependencies

- Python 3.10+
- LangGraph >= 0.0.19
- LangChain-AWS >= 0.1.0
- Boto3 >= 1.34.0
- Python-dotenv >= 1.0.0
- IPython >= 8.12.0



## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Acknowledgments

- Inspired by [Anthropic's guide on building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Special thanks to the AI/ML community

---

<div align="center">
Made with ❤️ by the Building_Agents team
</div>
