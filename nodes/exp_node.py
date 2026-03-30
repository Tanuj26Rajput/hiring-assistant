from state import GraphState
from prompts import exp_prompt
from llm import gemi_invoke
from .name_node import build_context_summary, get_last_user_message
import re

def validate_experience(experience: str) -> tuple[bool, str]:
    """Validate experience input"""
    experience = experience.strip()
    if not experience:
        return False, "Experience description cannot be empty. Please describe your work experience."
    
    if len(experience) < 10:
        return False, "Please provide a more detailed description of your work experience."
    
    if len(experience) > 2000:
        return False, "Experience description is too long. Please keep it under 2000 characters."
    
    return True, ""

def ask_exp(state: GraphState) -> GraphState:
    """Ask for candidate's work experience summary"""
    response = gemi_invoke(
        exp_prompt.format(phone=state.phone, context=build_context_summary(state))
    )
    state.messages.append({
        "role": "assistant",
        "content": response
    })
    state.stage = "ask_exp"
    return state

def process_exp(state: GraphState) -> GraphState:
    """Process candidate's experience input, validate it, and update state"""
    user_input = get_last_user_message(state)
    extract_exp_prompt = '''
        Extract only the person's work experience summary from the text.
        Text: {input}
        Return only the experience summary, nothing else.
    '''
    exp = gemi_invoke(extract_exp_prompt.format(input=user_input)).strip()
    is_valid, error_msg = validate_experience(exp)
    if not is_valid:
        state.messages.append({
            "role": "assistant",
            "content": error_msg
        })
        response = gemi_invoke(
            exp_prompt.format(phone=state.phone, context=build_context_summary(state))
        )
        state.messages.append({
            "role": "assistant",
            "content": response
        })
        state.stage = "ask_exp"
        return state
    
    state.exp = exp
    state.stage = "ask_role"
    return state
