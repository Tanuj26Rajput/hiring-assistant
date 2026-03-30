import json

import streamlit as st
from state import GraphState
from llm import gemi_invoke
from prompts import closing_prompt, fallback_prompt
from nodes.greet_node import greet_node
from nodes.name_node import ask_name_node, build_context_summary, process_name_node
from nodes.email_node import ask_email_node, process_email_node
from nodes.phone_node import ask_phone_number, process_phone_number
from nodes.exp_node import ask_exp, process_exp
from nodes.role_node import ask_role_node, process_role_node
from nodes.tech_stack_node import ask_tech_node, process_tech_node
from nodes.location import ask_location, process_location_node
from nodes.questions import ask_questions, process_questions

st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Plus+Jakarta+Sans:wght@400;500;700&display=swap');

        :root {
            --bg: #f5efe6;
            --paper: rgba(255, 250, 244, 0.88);
            --paper-strong: rgba(255, 252, 248, 0.96);
            --line: rgba(99, 76, 44, 0.14);
            --ink: #1f1a14;
            --muted: #6b5d4b;
            --accent: #d97706;
            --accent-soft: #fff1de;
            --accent-2: #0f766e;
            --shadow: 0 22px 60px rgba(84, 60, 24, 0.10);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(217, 119, 6, 0.16), transparent 28%),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.12), transparent 24%),
                linear-gradient(180deg, #faf5ee 0%, var(--bg) 100%);
            color: var(--ink);
            font-family: "Plus Jakarta Sans", sans-serif;
        }

        .main .block-container {
            max-width: 1240px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3 {
            font-family: "Manrope", sans-serif;
            letter-spacing: -0.03em;
            color: var(--ink);
        }

        .hero,
        .panel,
        .chat-wrap,
        .input-wrap {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 28px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(12px);
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 1.5rem 1.6rem;
            margin-bottom: 1rem;
        }

        .hero::after {
            content: "";
            position: absolute;
            top: -40px;
            right: -10px;
            width: 180px;
            height: 180px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(217, 119, 6, 0.18) 0%, transparent 70%);
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            background: var(--accent-soft);
            color: var(--accent);
            border-radius: 999px;
            padding: 0.36rem 0.72rem;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .hero-title {
            margin: 0.9rem 0 0.35rem;
            font-size: clamp(2rem, 4vw, 3.5rem);
            line-height: 0.95;
            max-width: 11ch;
        }

        .mini-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.8rem;
            margin-top: 1rem;
        }

        .mini-card {
            background: rgba(255, 255, 255, 0.58);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 0.9rem 1rem;
        }

        .mini-label {
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 800;
            color: var(--muted);
        }

        .mini-value {
            margin-top: 0.22rem;
            font-family: "Manrope", sans-serif;
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--ink);
        }

        .chat-wrap {
            padding: 1rem 1rem 0.35rem;
        }

        [data-testid="stChatMessageContent"] {
            border-radius: 20px;
            padding: 0.92rem 1rem;
            border: 1px solid rgba(31, 26, 20, 0.08);
            box-shadow: 0 12px 28px rgba(31, 26, 20, 0.04);
        }

        [data-testid="stChatMessage"]:has([aria-label="assistant message"]) [data-testid="stChatMessageContent"] {
            background: linear-gradient(180deg, #fffaf3 0%, #fff2e3 100%);
        }

        [data-testid="stChatMessage"]:has([aria-label="user message"]) [data-testid="stChatMessageContent"] {
            background: linear-gradient(180deg, rgba(15, 118, 110, 0.94) 0%, rgba(21, 128, 61, 0.90) 100%);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.14);
        }

        .input-wrap {
            margin-top: 1rem;
            padding: 1rem;
        }

        .input-title {
            margin: 0;
            font-family: "Manrope", sans-serif;
            font-size: 1.04rem;
            font-weight: 800;
        }

        .input-copy {
            margin: 0.25rem 0 0.85rem;
            color: var(--muted);
            font-size: 0.94rem;
        }

        .helper-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            margin-bottom: 0.75rem;
            padding: 0.34rem 0.7rem;
            border-radius: 999px;
            background: rgba(15, 118, 110, 0.10);
            color: var(--accent-2);
            font-size: 0.82rem;
            font-weight: 700;
        }

        .stTextInput input {
            border-radius: 16px !important;
            border: 1px solid rgba(31, 26, 20, 0.12) !important;
            background: rgba(255, 255, 255, 0.88) !important;
            color: var(--ink) !important;
            padding: 0.95rem 1rem !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        .stFormSubmitButton > button {
            width: 100%;
            border: none;
            border-radius: 16px;
            padding: 0.9rem 1rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
            color: white;
            box-shadow: 0 16px 28px rgba(15, 118, 110, 0.18);
        }

        .stDownloadButton > button {
            background: linear-gradient(135deg, #334155 0%, #0f766e 100%);
        }

        [data-testid="column"] .stButton > button {
            margin-top: 0.1rem;
        }

        @media (max-width: 900px) {
            .mini-grid {
                grid-template-columns: 1fr;
            }

            .main .block-container {
                padding-top: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

STAGE_DETAILS = {
    "ask_name": ("your full name", "candidate name collection"),
    "ask_email": ("your email address", "candidate email collection"),
    "ask_phone": ("your phone number", "candidate phone collection"),
    "ask_exp": ("your work experience summary", "candidate experience collection"),
    "ask_role": ("the role you want to apply for", "candidate desired role collection"),
    "ask_tech_stack": ("your tech stack and technical skills", "candidate tech stack collection"),
    "ask_location": ("your current location or city", "candidate location collection"),
    "ask_questions": ("your answers to the technical screening questions", "technical screening answers"),
}

ASK_NODE_HANDLERS = {
    "ask_name_node": ask_name_node,
    "ask_email": ask_email_node,
    "ask_phone": ask_phone_number,
    "ask_exp": ask_exp,
    "ask_role": ask_role_node,
    "ask_tech": ask_tech_node,
    "ask_location": ask_location,
    "ask_questions": ask_questions,
}


def reset_interview() -> None:
    st.session_state.state = GraphState()
    st.session_state.current_node = "greet"


def build_export_payload(state: GraphState) -> str:
    payload = {
        "name": state.name,
        "email": state.email,
        "phone": state.phone,
        "experience": state.exp,
        "role": state.role,
        "tech_stack": state.tech_stack,
        "location": state.location,
        "questions": state.questions,
        "answers": state.answers,
        "stage": state.stage,
        "messages": state.messages,
    }
    return json.dumps(payload, indent=2)


def render_header(state: GraphState) -> None:
    st.markdown(
        f"""
        <section class="hero">
            <div class="eyebrow">TalentScout Interview Workspace</div>
            <h1 class="hero-title">A cleaner screening experience for candidates and recruiters.</h1>
            <div class="mini-grid"></div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def is_unexpected_input(user_input: str, current_stage: str) -> bool:
    text = user_input.strip().lower()
    if not text or current_stage == "ask_questions":
        return False

    off_topic_markers = [
        "?",
        "what do you mean",
        "can you explain",
        "i do not understand",
        "i don't understand",
        "why do you need",
        "who are you",
        "help me",
        "tell me about",
    ]
    return any(marker in text for marker in off_topic_markers)


def append_fallback_response(state: GraphState, user_input: str) -> None:
    expected_input, current_step = STAGE_DETAILS.get(
        state.stage, ("the required screening detail", "screening step")
    )
    response = gemi_invoke(
        fallback_prompt.format(
            context=build_context_summary(state),
            current_step=current_step,
            expected_input=expected_input,
            user_input=user_input,
        )
    )
    state.messages.append({"role": "assistant", "content": response})


if "state" not in st.session_state:
    reset_interview()

state = st.session_state.state

if st.session_state.current_node == "greet":
    greet_node(state)
    st.session_state.current_node = "ask_name_node"

if st.session_state.current_node in ASK_NODE_HANDLERS:
    ASK_NODE_HANDLERS[st.session_state.current_node](state)
    st.session_state.current_node = "wait_user"

render_header(state)

action_col1, action_col2 = st.columns([0.2, 0.2], gap="small")
with action_col1:
    if st.button("Restart Interview", use_container_width=True):
        reset_interview()
        st.rerun()
with action_col2:
    st.download_button(
        "Download Summary",
        data=build_export_payload(state),
        file_name="talentscout_candidate_summary.json",
        mime="application/json",
        use_container_width=True,
    )

st.markdown('<section class="chat-wrap">', unsafe_allow_html=True)
for msg in state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
st.markdown("</section>", unsafe_allow_html=True)

if st.session_state.current_node == "wait_user":
    expected_input, _ = STAGE_DETAILS.get(
        state.stage, ("the next required screening detail", "screening step")
    )
    with st.form("candidate_response_form", clear_on_submit=True):
        user_input = st.text_input(
            "Your response",
            label_visibility="collapsed",
            placeholder=f"Type {expected_input} here...",
        )
        submitted = st.form_submit_button("Send Response")
    st.markdown("</section>", unsafe_allow_html=True)

    if submitted and user_input.strip():
        if is_unexpected_input(user_input, state.stage):
            state.messages.append({"role": "user", "content": user_input})
            append_fallback_response(state, user_input)
            st.rerun()

        state.messages.append({"role": "user", "content": user_input})
        current_stage = state.stage

        if current_stage == "ask_name":
            process_name_node(state)
            st.session_state.current_node = "ask_name_node" if state.stage == "ask_name" else "ask_email"
        elif current_stage == "ask_email":
            process_email_node(state)
            st.session_state.current_node = "ask_email" if state.stage == "ask_email" else "ask_phone"
        elif current_stage == "ask_phone":
            process_phone_number(state)
            st.session_state.current_node = "ask_phone" if state.stage == "ask_phone" else "ask_exp"
        elif current_stage == "ask_exp":
            process_exp(state)
            st.session_state.current_node = "ask_exp" if state.stage == "ask_exp" else "ask_role"
        elif current_stage == "ask_role":
            process_role_node(state)
            st.session_state.current_node = "ask_role" if state.stage == "ask_role" else "ask_tech"
        elif current_stage == "ask_tech_stack":
            process_tech_node(state)
            st.session_state.current_node = "ask_tech" if state.stage == "ask_tech_stack" else "ask_location"
        elif current_stage == "ask_location":
            process_location_node(state)
            st.session_state.current_node = "ask_location" if state.stage == "ask_location" else "ask_questions"
        elif current_stage == "ask_questions":
            process_questions(state)
            st.session_state.current_node = "ask_questions" if state.stage == "ask_questions" else "end"
        st.rerun()

if st.session_state.current_node == "end" and not state.closing_sent:
    response = gemi_invoke(
        closing_prompt.format(
            context=build_context_summary(state),
        )
    )
    state.messages.append({"role": "assistant", "content": response})
    state.closing_sent = True
    st.rerun()
