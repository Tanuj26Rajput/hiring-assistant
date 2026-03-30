from pydantic import BaseModel, Field
from typing import List

class GraphState(BaseModel):
    """Represents the state of the conversation graph.

    Attributes:
        messages (List[dict]): List of conversation messages with 'role' and 'content'.
        name (str): Candidate's name.
        email (str): Candidate's email.
        phone (str): Candidate's phone number.
        exp (str): Candidate's experience description.
        role (str): Desired role.
        tech_stack (str): Technical skills and technologies.
        location (str): Candidate's location.
        questions (str): Generated technical questions.
        answers (str): Candidate's answers to questions.
        stage (str): Current stage of the conversation.
    """
    messages: List[dict] = Field(default_factory=list)
    name: str = ""
    email: str = ""
    phone: str = ""
    exp: str = ""
    role: str = ""
    tech_stack: str = ""
    location: str = ""
    questions: str = ""
    answers: str = ""
    stage: str = "greet"
    closing_sent: bool = False
