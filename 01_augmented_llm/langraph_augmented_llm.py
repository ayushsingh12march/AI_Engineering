from pydantic import BaseModel, Field
from utils.llm_client import Claude3_7SonnetFactory


llm = Claude3_7SonnetFactory().create_client()

class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query that is optimized web search.")
    justification: str = Field(
        None, description="Why this query is relevant to the user's request."
    )


# Augment the LLM with schema for structured output
structured_llm = llm.with_structured_output(SearchQuery)

# Invoke the augmented LLM
output = structured_llm.invoke("How does Calcium CT score relate to high cholesterol?")
print(output)
####### Output #######
# search_query='relationship between calcium CT score coronary calcium scan and high cholesterol cardiovascular risk' 
# justification='This query is relevant as it seeks to understand the relationship between Calcium CT score (a measure of coronary artery calcification) and high cholesterol (a common cardiovascular risk factor). Understanding this relationship will help answer how these two medical indicators are connected in cardiovascular health assessment.'





############################################ Tool Calling Augmentatio ############################################

# Define a tool
def multiply(a: int, b: int) -> int:
    return a * b

# Augment the LLM with tools
llm_with_tools = llm.bind_tools([multiply])

# Invoke the LLM with input that triggers the tool call
msg = llm_with_tools.invoke("What is 2 times 3?")

# Get the tool call
print( "msg.tool_calls", msg.tool_calls)
####### Output #######
# msg.tool_calls [{'name': 'multiply', 'args': {'a': 2, 'b': 3}, 'id': 'toolu_bdrk_015LssQSex9FQLJ5sMMhhcpt', 'type': 'tool_call'}]


print("msg", msg) 
####### Output #######
# content='I can calculate that for you using the multiply function.'
# additional_kwargs={
#     'usage': {
#         'prompt_tokens': 389,
#           'completion_tokens': 80,
#             'cache_read_input_tokens': 0,
#               'cache_write_input_tokens': 0,
#                 'total_tokens': 469
#                 },
#     'stop_reason': 'tool_use',
#     'thinking': {},
#     'model_id': 'us.anthropic.claude-3-7-sonnet-20250219-v1:0',
#     'model_name': 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
#     } 
# response_metadata={
#     'usage': {
#         'prompt_tokens': 389,
#         'completion_tokens': 80,
#         'cache_read_input_tokens': 0,
#         'cache_write_input_tokens': 0,
#         'total_tokens': 469
#         },
#     'stop_reason': 'tool_use',
#     'thinking': {},
#     'model_id': 'us.anthropic.claude-3-7-sonnet-20250219-v1:0',
#     'model_name': 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
#     } 
# id='run--3593c002-cbc7-4e9c-8508-006528004435-0'
# tool_calls=[{'name': 'multiply', 'args': {'a': 2, 'b': 3}, 'id': 'toolu_bdrk_015LssQSex9FQLJ5sMMhhcpt', 'type': 'tool_call'}] 
# usage_metadata={
#     'input_tokens': 389,
#     'output_tokens': 80,
#     'total_tokens': 469,
#     'input_token_details': {'cache_creation': 0, 'cache_read': 0}
#     }


############################################ Memory Augmentation ############################################

# Define a simple memory store class
class ConversationMemory:
    def __init__(self):
        self.history = []
    
    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
    
    def get_conversation_history(self) -> str:
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.history])

# Create a memory instance
memory = ConversationMemory()

# Function to format conversation with memory
def format_with_memory(user_input: str, memory: ConversationMemory) -> str:
    history = memory.get_conversation_history()
    if history:
        return f"""Previous conversation:
{history}

Current user input: {user_input}

Please respond to the current input while considering the conversation history."""
    return user_input

# Example usage with memory
memory.add_message("user", "My name is Alice.")
memory.add_message("assistant", "Nice to meet you, Alice!")

# Create memory-augmented LLM
memory_llm = llm.with_config({"memory": memory})

# Test the memory augmentation
user_input = "What's my name?"
formatted_input = format_with_memory(user_input, memory)
response = memory_llm.invoke(formatted_input)

print("\nMemory Augmentation Example:")
print("User:", user_input)
print("Assistant:", response)

# Add the new interaction to memory
memory.add_message("user", user_input)
memory.add_message("assistant", str(response))

#Conversation history
print("Conversation history \n", memory.get_conversation_history())

####### Output #######
# user: My name is Alice.
# assistant: Nice to meet you, Alice!
# user: What's my name?
# assistant: content='Based on our previous conversation, your name is Alice. You shared that with me earlier.' additional_kwargs={'usage': {'prompt_tokens': 51, 'completion_tokens': 21, 'cache_read_input_tokens': 0, 'cache_write_input_tokens': 0, 'total_tokens': 72}, 'stop_reason': 'end_turn', 'thinking': {}, 'model_id': 'us.anthropic.claude-3-7-sonnet-20250219-v1:0', 'model_name': 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'} response_metadata={'usage': {'prompt_tokens': 51, 'completion_tokens': 21, 'cache_read_input_tokens': 0, 'cache_write_input_tokens': 0, 'total_tokens': 72}, 'stop_reason': 'end_turn', 'thinking': {}, 'model_id': 'us.anthropic.claude-3-7-sonnet-20250219-v1:0', 'model_name': 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'} id='run--648edb2e-808d-464d-aa93-692f8001afbe-0' usage_metadata={'input_tokens': 51, 'output_tokens': 21, 'total_tokens': 72, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}