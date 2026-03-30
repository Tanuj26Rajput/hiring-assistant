from state import GraphState
from prompts import email_prompt
from llm import gemi_invoke
from .name_node import build_context_summary, get_last_user_message
import re

def validate_email(email: str) -> tuple[bool, str]:
    """Validate email input"""
    email = email.strip()
    if not email:
        return False, "Email cannot be empty. Please provide your email address."
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Please provide a valid email address (e.g., user@example.com)."
    
    return True, ""

def ask_email_node(state: GraphState) -> GraphState:
    """Ask for candidate's email address"""
    response = gemi_invoke(
        email_prompt.format(name=state.name, context=build_context_summary(state))
    )
    state.messages.append({
        "role": "assistant",
        "content": response
    })
    state.stage = "ask_email"
    return state

def process_email_node(state: GraphState) -> GraphState:
    """Process candidate's email input, validate it, and update state"""
    user_input = get_last_user_message(state)
    extract_email_prompt = '''
        Extract only the person's email address from the text.
        Text: {input}
        Return only the email, nothing else.
    '''
    email = gemi_invoke(extract_email_prompt.format(input=user_input)).strip()
    is_valid, error_msg = validate_email(email)
    if not is_valid:
        state.messages.append({
            "role": "assistant",
            "content": error_msg
        })
        response = gemi_invoke(
            email_prompt.format(name=state.name, context=build_context_summary(state))
        )
        state.messages.append({
            "role": "assistant",
            "content": response
        })
        state.stage = "ask_email"
        return state
    
    state.email = email
    state.stage = "ask_phone"
    return state
