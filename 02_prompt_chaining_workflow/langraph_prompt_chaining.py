

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from utils.llm_client import Claude3_7SonnetFactory



llm = Claude3_7SonnetFactory().create_client()

class State(TypedDict):
    topic: str
    joke: str
    improve_joke: str
    polished_joke: str



def generate_joke(state: State):
    """First LLM call to generate the joke"""
    
    msg = llm.invoke(f"Write a joke about {state['topic']}")
    return {"joke": msg.content}


def improve_joke(state: State):
    """Second LLM call to improve the joke"""
    
    msg = llm.invoke(f"Make this joke funnier by mocking the punchline: {state['joke']}")
    return {"improve_joke": msg.content}

def polish_joke(state: State):
    """Third LLM call to polish the joke"""
    
    msg = llm.invoke(f"Add a surprising twist to the joke: {state['improve_joke']}")
    return {"polished_joke": msg.content}


def check_punchline(state: State):
    """Gate function to check if the joke has a punchline"""

    # Simple check - does the joke contain "?" or "!"
    if "?" in state["joke"] or "!" in state["joke"]:
        return "Pass"
    return "Fail"


workflow = StateGraph(State)

workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_node("polish_joke", polish_joke)


workflow.add_edge(START, "generate_joke")
workflow.add_conditional_edges(
    "generate_joke",
    check_punchline,
    {
        "Fail": "improve_joke",
        "Pass": END
    }
)

workflow.add_edge("improve_joke", "polish_joke")
workflow.add_edge("polish_joke", END)



# Compile
chain = workflow.compile()


# Show workflow in terminal
print("\nWorkflow Graph:")
print(chain.get_graph().draw_mermaid())


# Invoke
state = chain.invoke({"topic": "Software Engineers"})
print(state)