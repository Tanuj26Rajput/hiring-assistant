from nodes.greet_node import greet_node
from nodes.name_node import ask_name, process_name_node
from nodes.email_node import ask_email, process_email_node
from nodes.phone_node import ask_phone, process_phone_node
from nodes.exp_node import ask_exp, process_exp
from nodes.role_node import ask_role, process_role_node
from nodes.tech_stack_node import ask_tech_stack, process_tech_node
from nodes.location import ask_location, process_location_node
from nodes.questions import ask_questions, process_questions

from state import GraphState

from langgraph import StateGraph

def router(state: GraphState) -> str:
    return state.stage

builder = StateGraph(GraphState)

builder.add_node("greet", greet_node)
builder.add_node("ask_name", ask_name)
builder.add_node("process_name", process_name_node)
builder.add_node("ask_email", ask_email)
builder.add_node("process_email", process_email_node)
builder.add_node("ask_phone", ask_phone)
builder.add_node("process_phone", process_phone_node)
builder.add_node("ask_exp", ask_exp)
builder.add_node("process_exp", process_exp)
builder.add_node("ask_role", ask_role)
builder.add_node("process_role", process_role_node)
builder.add_node("ask_tech", ask_tech_stack)
builder.add_node("process_tech", process_tech_node)
builder.add_node("ask_location", ask_location)
builder.add_node("process_location", process_location_node)
builder.add_node("ask_questions", ask_questions)
builder.add_node("process_questions", process_questions)

builder.set_entry_point("greet")
builder.add_edge("greet", "ask_name")
builder.add_edge("ask_name", "process_name")
builder.add_conditional_edges(
    "process_name", router, {
        "process_name": "process_name",
        "ask_email": "ask_email"
    }
)
builder.add_edge("ask_email", "process_email")
builder.add_conditional_edges(
    "process_email", router, {
        "process_email": "process_email",
        "ask_phone": "ask_phone"
    }
)
builder.add_edge("ask_phone", "process_phone")
builder.add_conditional_edges(
    "process_phone", router, {
        "process_phone": "process_phone",
        "ask_exp": "ask_exp"
    }
)
builder.add_edge("ask_exp", "process_exp")
builder.add_conditional_edges(
    "process_exp", router, {
        "process_exp": "process_exp",
        "ask_role": "ask_role"
    }
)
builder.add_edge("ask_role", "process_role")
builder.add_conditional_edges(
    "process_role", router, {
        "process_role": "process_role",
        "ask_tech": "ask_tech"
    }
)
builder.add_edge("ask_tech", "process_tech")
builder.add_conditional_edges(
    "process_tech", router, {
        "process_tech": "process_tech",
        "ask_location": "ask_location"
    }
)
builder.add_edge("ask_location", "process_location")
builder.add_conditional_edges(
    "process_location", router, {
        "process_location": "process_location",
        "ask_questions": "ask_questions"
    }
)
builder.add_edge("ask_questions", "process_questions")
builder.add_conditional_edges(
    "process_questions", router, {
        "process_questions": "process_questions",
        "end": "end"
    }
)

workflow = builder.compile()