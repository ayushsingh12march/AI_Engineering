
from typing import TypedDict
from utils.llm_client import Claude3_7SonnetFactory
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    topic: str
    poem: str
    story: str
    joke: str
    combined_result: str


llm = Claude3_7SonnetFactory().create_client()


def poem_writer(state: State):
    result = llm.invoke(f"Write a poem about {state['topic']}")
    return {"poem": result.content}


def story_writer(state: State):
    result = llm.invoke(f"Write a story about {state['topic']}")
    return {"story": result.content}


def joke_writer(state: State):
    result = llm.invoke(f"Write a joke about {state['topic']}")
    return {"joke": result.content}


def aggregate_results(state: State):
    """Combine the joke and story into a single output"""
    combined = f"Here is the combined result on the topic {state['topic']}: \n Poem: {state['poem']} \n Story: {state['story']} \n Joke: {state['joke']}"
    return {"combined_result": combined}


parallel_builder = StateGraph(State)

parallel_builder.add_node("poem_writer", poem_writer)
parallel_builder.add_node("story_writer", story_writer)
parallel_builder.add_node("joke_writer", joke_writer)
parallel_builder.add_node("aggregate_results", aggregate_results)

parallel_builder.add_edge(START, "poem_writer")
parallel_builder.add_edge(START, "story_writer")
parallel_builder.add_edge(START, "joke_writer")
parallel_builder.add_edge("poem_writer", "aggregate_results")
parallel_builder.add_edge("story_writer", "aggregate_results")
parallel_builder.add_edge("joke_writer", "aggregate_results")

parallel_builder.add_edge("aggregate_results", END)

parallel_workflow = parallel_builder.compile()


# Show workflow in terminal
print("\nWorkflow Graph:")
print(parallel_workflow.get_graph().draw_mermaid())

# Invoke
state = parallel_workflow.invoke({"topic": "Software Engineers"})
print(state)
