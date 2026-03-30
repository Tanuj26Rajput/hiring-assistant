from state import GraphState
from prompts import role_prompt
from llm import gemi_invoke
from .name_node import build_context_summary, get_last_user_message

def validate_role(role: str) -> tuple[bool, str]:
    """Validate role input"""
    role = role.strip()
    if not role:
        return False, "Role cannot be empty. Please specify the role you're interested in."
    
    if len(role) < 2:
        return False, "Role seems too short. Please provide a more specific role."
    
    if len(role) > 100:
        return False, "Role description is too long. Please keep it concise."
    
    return True, ""

def ask_role_node(state: GraphState) -> GraphState:
    """Ask for candidate's desired role"""
    response = gemi_invoke(
        role_prompt.format(exp=state.exp, context=build_context_summary(state))
    )
    state.messages.append({
        "role": "assistant",
        "content": response
    })
    state.stage = "ask_role"
    return state

def process_role_node(state: GraphState) -> GraphState:
    """Process candidate's desired role input, validate it, and update state"""
    user_input = get_last_user_message(state)
    extract_role_prompt = '''
        Extract only the person's desired role from the text.
        Text: {input}
        Return only the desired role, nothing else.
    '''
    role = gemi_invoke(extract_role_prompt.format(input=user_input)).strip()
    is_valid, error_msg = validate_role(role)
    if not is_valid:
        state.messages.append({
            "role": "assistant",
            "content": error_msg
        })
        response = gemi_invoke(
            role_prompt.format(exp=state.exp, context=build_context_summary(state))
        )
        state.messages.append({
            "role": "assistant",
            "content": response
        })
        state.stage = "ask_role"
        return state
    
    state.role = role
    state.stage = "ask_tech_stack"
    return state
