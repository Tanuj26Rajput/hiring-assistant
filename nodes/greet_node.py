from state import GraphState
from prompts import greeting_prompt
from llm import gemi_invoke
import state 

def greet_node(state: GraphState):    
    """Greet the user and initialize the conversation by setting the stage to 'name'."""    
    response = gemi_invoke(greeting_prompt.format())
    state.messages.append({
        "role": "assistant",
        "content": response.strip()
    })
    state.stage = "ask_name"
    return state
