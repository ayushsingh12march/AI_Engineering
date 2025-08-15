from typing import TypedDict
from typing_extensions import Literal
from pydantic import BaseModel, Field
from utils.llm_client import Claude3_7SonnetFactory
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

llm = Claude3_7SonnetFactory().create_client()


# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(None, description="The step to take")


# Augment the LLM with schema for structured output
router_llm = llm.with_structured_output(Route)

class State(TypedDict):
    input: str
    decision: str
    output: str


def story_writer(state: State):
    
    result = llm.invoke(f"{state['input']}")
    return {"output": result.content}


def poem_writer(state: State):
    
    result = llm.invoke(f"{state['input']}")
    return {"output": result.content}


def joke_writer(state: State):
    
    result = llm.invoke(f"{state['input']}")
    return {"output": result.content}



def router(state: State):
    
    # Run the augmented LLM with structured output to serve as routing logic
    decision = router_llm.invoke([
        SystemMessage(content="You are a routing agent. You are given a user input and you need to decide which step to take."),
        HumanMessage(content=state["input"])
    ])
    return {"decision": decision.step}


# Conditional edge function to route to the appropriate node
def route_decision(state: State):
    # Return the node name you want to visit next
    if state["decision"] == "poem":
        return "poem_writer"
    elif state["decision"] == "story":
        return "story_writer"
    elif state["decision"] == "joke":
        return "joke_writer"


router_builder = StateGraph(State)

router_builder.add_node("router", router)
router_builder.add_node("poem_writer", poem_writer)
router_builder.add_node("story_writer", story_writer)
router_builder.add_node("joke_writer", joke_writer)

router_builder.add_edge(START, "router")
router_builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "poem_writer": "poem_writer",
        "story_writer": "story_writer",
        "joke_writer": "joke_writer",
    }
)

router_builder.add_edge("poem_writer", END)
router_builder.add_edge("story_writer", END)
router_builder.add_edge("joke_writer", END)

# Compile workflow
router_workflow = router_builder.compile()


# Show workflow in terminal
print("\nWorkflow Graph:")
print(router_workflow.get_graph().draw_mermaid())

# Invoke
state = router_workflow.invoke({"input": "Write me a poem about stock market and life of a software engineer"})
print(state)
