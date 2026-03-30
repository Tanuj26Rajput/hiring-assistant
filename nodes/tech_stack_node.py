from state import GraphState
from prompts import tech_stack_prompt
from llm import gemi_invoke
from .name_node import build_context_summary, get_last_user_message

def validate_tech_stack(tech_stack: str) -> tuple[bool, str]:
    """Validate tech stack input"""
    tech_stack = tech_stack.strip()
    if not tech_stack:
        return False, "Tech stack cannot be empty. Please list your technical skills."
    
    if len(tech_stack) < 3:
        return False, "Tech stack seems too short. Please provide more details about your technical skills."
    
    if len(tech_stack) > 1000:
        return False, "Tech stack description is too long. Please keep it under 1000 characters."
    
    return True, ""

def ask_tech_node(state: GraphState) -> GraphState:
    """Ask for candidate's tech stack"""
    response = gemi_invoke(
        tech_stack_prompt.format(role=state.role, context=build_context_summary(state))
    )
    state.messages.append({
        "role": "assistant",
        "content": response
    })
    state.stage = "ask_tech_stack"
    return state

def process_tech_node(state: GraphState) -> GraphState:
    """Process candidate's tech stack input, validate it, and update state"""
    user_input = get_last_user_message(state)
    extract_phone_prompt = '''
        Extract only the person's tech stack from the text.
        Text: {input}
        Return only the tech stack, nothing else.
    '''
    tech_stack = gemi_invoke(extract_phone_prompt.format(input=user_input)).strip()
    is_valid, error_msg = validate_tech_stack(tech_stack)
    if not is_valid:
        state.messages.append({
            "role": "assistant",
            "content": error_msg
        })
        response = gemi_invoke(
            tech_stack_prompt.format(role=state.role, context=build_context_summary(state))
        )
        state.messages.append({
            "role": "assistant",
            "content": response
        })
        state.stage = "ask_tech_stack"
        return state
    
    state.tech_stack = tech_stack
    state.stage = "ask_location"
    return state
