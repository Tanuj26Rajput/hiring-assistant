from state import GraphState
from prompts import questions_prompt
from llm import gemi_invoke
from .name_node import build_context_summary, get_last_user_message

def ask_questions(state: GraphState) -> GraphState:
    """Ask the candidate a set of questions based on the collected information (role, tech stack, location, experience)"""
    response = gemi_invoke(
        questions_prompt.format(
            context=build_context_summary(state),
            location=state.location,
            tech_stack=state.tech_stack,
            role=state.role,
            exp=state.exp,
        )
    )
    state.messages.append({
        "role": "assistant",
        "content": response
    })
    state.stage = "ask_questions"
    state.questions = response.strip().split("\n")
    return state

def process_questions(state: GraphState) -> GraphState:
    """Process candidate's answers to questions, validate them, and update state"""
    user_input = get_last_user_message(state)
    state.answers = user_input.strip()
    state.stage = "end"
    return state
