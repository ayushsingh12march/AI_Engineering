
import operator
from typing import Annotated, List, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Send
from utils.llm_client import Claude3_7SonnetFactory
from langgraph.graph import StateGraph, START, END


class Section(BaseModel):
    name: str = Field(description="Name for this section of the report")
    description: str = Field(description="Brief Overview of the topics and concepts to be covered in this section")


class Sections(BaseModel):
    sections: List[Section] = Field(description="List of sections of the report report")


llm = Claude3_7SonnetFactory().create_client()


# Augment the LLM with schema for structured output
planner = llm.with_structured_output(Sections)



# Graph state
class State(TypedDict):
    topic: str # Report topic
    sections: list[Section] # List of report sections
    completed_sections: Annotated[list, operator.add] # All workers write to this key in parallel
    final_report: str # Final report


# Worker state
class WorkerState(TypedDict):
    section: Section 
    completed_sections: Annotated[list, operator.add]



# Nodes
def orchestrator(state: State):
    """Orchestrator that generates a plan for the report"""

    # Generate queries
    report_sections = planner.invoke([
        SystemMessage(content="Generate a plan for the report"),
        HumanMessage(content=f"Here is the topic of the report: {state['topic']}")
    ])

    return {"sections" : report_sections.sections}


def llm_worker(state: WorkerState):
    """Worker writes a section of the report"""

    # Generate the section
    section = llm.invoke([
        SystemMessage(content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."),
        HumanMessage(content=f"Here is the section name: {state['section'].name} and the section description: {state['section'].description}")
    ])

    # Write the updated section to completed sections
    return {"completed_sections": [section.content]}


def synthesizer(state: State):
    """Synthesize full report from the sections"""

    # List of completed sections
    completed_sections = state["completed_sections"]

    # Format completed section to str to use as context for final sections
    completed_report = "\n-----------\n".join(completed_sections)

    return {"final_report": completed_report}




# Creating Workers in LangGraph

# Because orchestrator-worker workflows are common, LangGraph has the Send API to support this. It lets you dynamically create worker nodes and send each one a specific input. Each worker has its own state, and all worker outputs are written to a shared state key that is accessible to the orchestrator graph. This gives the orchestrator access to all worker output and allows it to synthesize them into a final output. As you can see below, we iterate over a list of sections and Send each to a worker node.

# Conditional edge function to create llm_workers that each write a section of report
def assign_worker(state: State):
    """Assign a worker to write a section of the report"""

    # Kick off section writing in parallel via Send() API
    return [Send("llm_worker", {"section": section}) for section in state["sections"]]






# Build workflow
orchestrator_worker_builder = StateGraph(State)

#Add the nodes
orchestrator_worker_builder.add_node("orchestrator", orchestrator)
orchestrator_worker_builder.add_node("llm_worker", llm_worker)
orchestrator_worker_builder.add_node("synthesizer", synthesizer)

# Add edges
orchestrator_worker_builder.add_edge(START, "orchestrator")
orchestrator_worker_builder.add_conditional_edges(
    "orchestrator",
    assign_worker,
    ["llm_worker"]
)
orchestrator_worker_builder.add_edge("llm_worker", "synthesizer")
orchestrator_worker_builder.add_edge("synthesizer", END)

# Compile workflow
orchestrator_worker_workflow = orchestrator_worker_builder.compile()


# Show workflow in terminal
print("\nWorkflow Graph:")
print(orchestrator_worker_workflow.get_graph().draw_mermaid())



# Invoke
state = orchestrator_worker_workflow.invoke({"topic": "Create a report on Agentic RAG vs ReRanker RAG"})

print(state)
