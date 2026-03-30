from state import GraphState
from prompts import location_prompt
from llm import gemi_invoke
from .name_node import build_context_summary, get_last_user_message

def validate_location(location: str) -> tuple[bool, str]:
    """Validate location input"""
    location = location.strip()
    if not location:
        return False, "Location cannot be empty. Please provide your location."
    
    if len(location) < 2:
        return False, "Location seems too short. Please provide a more specific location."
    
    if len(location) > 100:
        return False, "Location description is too long. Please keep it concise."
    
    return True, ""

def ask_location(state: GraphState) -> GraphState:
    """Ask for candidate's location"""
    response = gemi_invoke(
        location_prompt.format(
            tech_stack=state.tech_stack,
            context=build_context_summary(state),
        )
    )
    state.messages.append({
        "role": "assistant",
        "content": response
    })
    state.stage = "ask_location"
    return state

def process_location_node(state: GraphState) -> GraphState:
    """Process candidate's location input, validate it, and update state"""
    user_input = get_last_user_message(state)
    extract_location_prompt = '''
        Extract only the person's location from the text.
        Text: {input}
        Return only the location, nothing else.
    '''
    location = gemi_invoke(extract_location_prompt.format(input=user_input)).strip()
    is_valid, error_msg = validate_location(location)
    if not is_valid:
        state.messages.append({
            "role": "assistant",
            "content": error_msg
        })
        response = gemi_invoke(
            location_prompt.format(
                tech_stack=state.tech_stack,
                context=build_context_summary(state),
            )
        )
        state.messages.append({
            "role": "assistant",
            "content": response
        })
        state.stage = "ask_location"
        return state
    
    state.location = location
    state.stage = "ask_questions"
    return state
