from datetime import datetime
from typing import Literal
from langchain.chat_models import init_chat_model
from langgraph.types import Command
from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string
from settings import CLAUDE_3_7_SONNET_MODEL_ID, AWS_REGION
from langgraph.graph import StateGraph, START, END

import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state_scope import AgentState, AgentInputState
from prompts import clarify_with_user_instructions, transform_messages_into_research_topic_prompt
from state_scope import ClarifyWithUser, ResearchQuestion
from langgraph.checkpoint.memory import InMemorySaver







# ===== UTILITY FUNCTIONS =====

def get_today_str() -> str:
    """Get current date in a human-readable format."""
    return datetime.now().strftime("%a %b %-d, %Y")

# ===== CONFIGURATION =====

# Initialize model
model = init_chat_model(model=CLAUDE_3_7_SONNET_MODEL_ID,
                        model_provider="bedrock",
                        region_name=AWS_REGION,
                        temperature=0.0)


# ===== WORKFLOW NODES =====
def clarify_with_user(state: AgentState) -> Command[Literal["write_research_brief","__end__"]]:

    structured_output_model = model.with_structured_output(ClarifyWithUser)

    response = structured_output_model.invoke([
        HumanMessage(content=clarify_with_user_instructions.format(
            messages=get_buffer_string(messages=state["messages"]),
            date=get_today_str(),
        ))
    ])


    # Route based on clarification need
    if response.need_clarification:
        return Command(
            goto=END,
            update={"messages": [AIMessage(content=response.question)]}
        )
    else:
        return Command(
            goto="write_research_brief",
            update={"messages": [AIMessage(content=response.verification)]}
        )

def write_research_brief(state: AgentState):
    """
    Transform the conversation history into a comprehensive research brief.
    
    Uses structured output to ensure the brief follows the required format
    and contains all necessary details for effective research.
    """

    structured_output_model = model.with_structured_output(ResearchQuestion)

    response = structured_output_model.invoke([
        HumanMessage(content=transform_messages_into_research_topic_prompt.format(
            messages=get_buffer_string(messages=state["messages"]),
            date=get_today_str(),
        ))
    ])

    # Update state with generated research brief and pass it to the supervisor
    return {
        "research_brief": response.research_brief,
        "supervisor_messages": [HumanMessage(content=f"{response.research_brief}.")]
    }

# ===== GRAPH CONSTRUCTION =====

# Build the scoping workflow
deep_research_builder = StateGraph(AgentState, input=AgentInputState)

# Add workflow nodes
deep_research_builder.add_node("clarify_with_user", clarify_with_user)
deep_research_builder.add_node("write_research_brief", write_research_brief)

# Add edges
deep_research_builder.add_edge(START, "clarify_with_user")
deep_research_builder.add_edge("write_research_brief", END)

# Compile the workflow
scope_research = deep_research_builder.compile()



# Run the workflow
checkpointer = InMemorySaver()
scope = deep_research_builder.compile(checkpointer=checkpointer)
thread = {"configurable": {"thread_id": "1"}}
result = scope.invoke({"messages": [HumanMessage(content="I want to research the best coffee shops in San Francisco.")]}, config=thread)
print(result)
# {'messages': 
# [HumanMessage(content='I want to research the best coffee shops in San Francisco.', additional_kwargs={}, response_metadata={}, id='75771c37-69c7-490b-ac27-c3aa6cca062c'),
#  AIMessage(content='To provide you with the best research on coffee shops in San Francisco, could you please clarify:\n\n1. Are you looking for any specific type of coffee shops (e.g., specialty coffee, coffee shops with food options, coffee shops good for working)?\n2. Do you have any specific areas of San Francisco in mind?\n3. Are there any particular criteria that matter most to you (e.g., coffee quality, ambiance, price, Wi-Fi availability)?',
# 
# 
#  additional_kwargs={}, response_metadata={}, id='ecac0fca-75e3-4602-a0c1-56681247c594')], 'supervisor_messages': []}

print("--------------------------------")


result = scope.invoke({"messages": [HumanMessage(content="Let's examine coffee quality to assess the best coffee shops in San Francisco. Don't ask more questions")]}, config=thread)
print(result)
# {'messages': 
# [HumanMessage(content='I want to research the best coffee shops in San Francisco.', additional_kwargs={}, response_metadata={}, id='75771c37-69c7-490b-ac27-c3aa6cca062c'),
#  
# AIMessage(content='To provide you with the best research on coffee shops in San Francisco, could you please clarify:\n\n1. Are you looking for any specific type of coffee shops (e.g., specialty coffee, coffee shops with food options, coffee shops good for working)?\n2. Do you have any specific areas of San Francisco in mind?\n3. Are there any particular criteria that matter most to you (e.g., coffee quality, ambiance, price, Wi-Fi availability)?', additional_kwargs={}, response_metadata={}, id='ecac0fca-75e3-4602-a0c1-56681247c594'), 
# 
# HumanMessage(content="Let's examine coffee quality to assess the best coffee shops in San Francisco. Don't ask more questions", additional_kwargs={}, response_metadata={}, id='e5ce5c5e-7dab-4606-ad3d-e0370cf0e470'),
# 
# AIMessage(content="I understand that you want me to research the best coffee shops in San Francisco specifically focusing on coffee quality as the main criterion. I have sufficient information to begin this research without asking additional questions. I'll now start gathering information about San Francisco coffee shops known for their exceptional coffee quality.", additional_kwargs={}, response_metadata={}, id='7f5390b4-ea52-4902-a550-9defb1c32f0b')], 
# 
# 'research_brief': "I want to research the best coffee shops in San Francisco specifically focusing on coffee quality as the primary criterion. Please evaluate coffee shops across the city based on factors that determine exceptional coffee quality (such as bean sourcing, roasting methods, brewing techniques, freshness, and flavor profiles). I'm interested in the entire San Francisco area without any specific neighborhood restrictions. No need to prioritize other factors like ambiance, price, or Wi-Fi availability unless they directly impact the coffee quality assessment. Please provide information from reputable sources such as specialty coffee publications, barista reviews, and official coffee shop websites rather than general review aggregators.", 
# 'supervisor_messages': [HumanMessage(content="I want to research the best coffee shops in San Francisco specifically focusing on coffee quality as the primary criterion. Please evaluate coffee shops across the city based on factors that determine exceptional coffee quality (such as bean sourcing, roasting methods, brewing techniques, freshness, and flavor profiles). I'm interested in the entire San Francisco area without any specific neighborhood restrictions. No need to prioritize other factors like ambiance, price, or Wi-Fi availability unless they directly impact the coffee quality assessment. Please provide information from reputable sources such as specialty coffee publications, barista reviews, and official coffee shop websites rather than general review aggregators..", additional_kwargs={}, response_metadata={}, id='855caa41-3220-4c68-ae48-de31273079fa')]}

print("--------------------------------")

print(result["research_brief"])







