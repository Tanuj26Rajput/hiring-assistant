from state import GraphState
from prompts import phone_prompt
from llm import gemi_invoke
from .name_node import build_context_summary, get_last_user_message
import re

def validate_phone(phone: str) -> tuple[bool, str]:
    """Validate phone number input"""
    phone = phone.strip()
    if not phone:
        return False, "Phone number cannot be empty. Please provide your phone number."
    
    # Remove common separators and check for digits
    clean_phone = re.sub(r'[\s\-\(\)\.\+]', '', phone)
    
    if not clean_phone.isdigit():
        return False, "Phone number should contain only digits, spaces, hyphens, parentheses, and plus signs."
    
    if len(clean_phone) < 10 or len(clean_phone) > 15:
        return False, "Phone number should be between 10 and 15 digits long."
    
    return True, ""

def ask_phone_number(state: GraphState) -> GraphState:
    """Ask for candidate's phone number"""
    response = gemi_invoke(
        phone_prompt.format(email=state.email, context=build_context_summary(state))
    )
    state.messages.append({
        "role": "assistant",
        "content": response
    })
    state.stage = "ask_phone"
    return state

def process_phone_number(state: GraphState) -> GraphState:
    """Process candidate's phone number input, validate it, and update state"""
    user_input = get_last_user_message(state)
    extract_phone_prompt = '''
        Extract only the person's phone number from the text.
        Text: {input}
        Return only the phone number, nothing else.
    '''
    phone = gemi_invoke(extract_phone_prompt.format(input=user_input)).strip()
    is_valid, error_msg = validate_phone(phone)
    if not is_valid:
        state.messages.append({
            "role": "assistant",
            "content": error_msg
        })
        response = gemi_invoke(
            phone_prompt.format(email=state.email, context=build_context_summary(state))
        )
        state.messages.append({
            "role": "assistant",
            "content": response
        })
        state.stage = "ask_phone"
        return state
    
    state.phone = phone
    state.stage = "ask_exp"
    return state

