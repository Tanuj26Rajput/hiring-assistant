from state import GraphState
from prompts import name_prompt
from llm import gemi_invoke
import re

def get_last_user_message(state):
    for msg in reversed(state.messages):
        if msg['role'] == "user":
            return msg['content']
    return ""

def build_context_summary(state: GraphState) -> str:
    """Build a summary of collected candidate details to provide context for LLM prompts."""
    context_items = []
    if state.name:
        context_items.append(f"Name: {state.name}")
    if state.email:
        context_items.append(f"Email: {state.email}")
    if state.phone:
        context_items.append(f"Phone: {state.phone}")
    if state.exp:
        context_items.append(f"Experience: {state.exp}")
    if state.role:
        context_items.append(f"Desired role: {state.role}")
    if state.tech_stack:
        context_items.append(f"Tech stack: {state.tech_stack}")
    if state.location:
        context_items.append(f"Location: {state.location}")
    if not context_items:
        return "No candidate details collected yet."
    return "\n".join(context_items)

def validate_name(name: str) -> tuple[bool, str]:
    """Validate name input"""
    name = name.strip()
    if not name:
        return False, "Name cannot be empty. Please provide your full name."
    
    if len(name) < 2:
        return False, "Name seems too short. Please provide your full name."
    
    if len(name) > 100:
        return False, "Name seems too long. Please provide a reasonable name."
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return False, "Name contains invalid characters. Please use only letters, spaces, hyphens, and apostrophes."
    
    return True, ""

def ask_name_node(state: GraphState) -> GraphState:
    """Ask for candidate's name"""
    response = gemi_invoke(name_prompt.format(context=build_context_summary(state)))
    state.messages.append({
        "role": "assistant",
        "content": response
    })
    state.stage = "ask_name"
    return state

def process_name_node(state: GraphState):
    """Process candidate's name input, validate it, and update state"""
    user_input = get_last_user_message(state)
    EXTRACT_NAME_PROMPT = """
        Extract only the person's full name from the text.

        Text: "{input}"

        Return ONLY the name, nothing else.
    """
    name = gemi_invoke(EXTRACT_NAME_PROMPT.format(input=user_input)).strip()
    is_valid, error_msg = validate_name(name)
    if not is_valid:
        state.messages.append({
            "role": "assistant",
            "content": error_msg
        })
        response = gemi_invoke(name_prompt.format(context=build_context_summary(state)))
        state.messages.append({
            "role": "assistant",
            "content": response
        })
        state.stage = "ask_name"
        return state
    
    state.name = name
    state.stage = "ask_email"
    return state
