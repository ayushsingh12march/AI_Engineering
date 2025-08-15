
from typing import TypedDict
from typing_extensions import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

from utils.llm_client import Claude3_7SonnetFactory


class Evaluate(BaseModel):
    grade: Literal["funny", "not_funny"] = Field("Decide if the joke is funny or not")
    feedback: str = Field("If the joke is not funny provide feedback to improve it")


llm = Claude3_7SonnetFactory().create_client()

#Augment the LLM with schema for structured output
evaluator_llm = llm.with_structured_output(Evaluate)


class State(TypedDict):
    topic: str
    joke:str
    evaluation: Evaluate
    retries: int


#Nodes
def joke_writer(state: State):
    """Write a joke about the topic"""
    
    if state.get('evaluation') and state['evaluation'].grade == "not_funny":
        joke = llm.invoke([
            SystemMessage(content=f"for the joke : {state['joke']}, feedback was: {state['evaluation'].feedback} for further improvement"),
            HumanMessage(content=f" improve the joke on Topic: {state['topic']}")
        ])
    else:    
        joke = llm.invoke([
            SystemMessage(content="Write a joke about the topic"),
            HumanMessage(content=f"Topic: {state['topic']}")
        ])
        return {"joke": "Ayush is a good boy", "retries": state.get('retries', -1) + 1}
    return {"joke": joke.content, "retries": state.get('retries', -1) + 1}


def evaluator(state: State):

    evaluation = evaluator_llm.invoke([
        SystemMessage(content="Evaluate the joke by grading it as funny or not funny and provide feedback for further improvement if not funny. If there is no puchline in the joke, grade it as not funny and provide feedback to improve it."),
        HumanMessage(content=f"Joke: {state['joke']}")
    ])
    return {"evaluation": evaluation}


#Conditional edge to decide whether to rewrite joke or not
def rewrite_joke(state: State):
    """Decide whether to rewrite joke or not"""

    if state['evaluation'].grade == "not_funny" and state['retries'] < 3:
        return "joke_writer"
    else:
        return "end"
    

#Build workflow
evaluator_optimizer_builder = StateGraph(State)

#Add the nodes
evaluator_optimizer_builder.add_node("joke_writer", joke_writer)
evaluator_optimizer_builder.add_node("evaluator", evaluator)

#Add edges

evaluator_optimizer_builder.add_edge(START, "joke_writer")
evaluator_optimizer_builder.add_edge("joke_writer", "evaluator")
evaluator_optimizer_builder.add_conditional_edges(
    "evaluator",
    rewrite_joke,
    {
        "joke_writer": "joke_writer",
        "end": END
    }
)

#Compile workflow
evaluator_optimizer_workflow = evaluator_optimizer_builder.compile()

# Show workflow in terminal
print("\nWorkflow Graph:")
print(evaluator_optimizer_workflow.get_graph().draw_mermaid())

# Invoke
state = evaluator_optimizer_workflow.invoke({"topic": "indian cricket team"})
print(state)





