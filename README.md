# Hiring Assistant Chatbot

## Project Overview

The Hiring Assistant is an AI-powered chatbot developed for TalentScout, a recruitment agency specializing in technology placements. It conducts initial screenings of job candidates by:

- Gathering essential information: name, email, phone, location, experience, desired role, and technical skills.
- Generating relevant technical questions based on the candidate's declared tech stack.
- Providing a conversational interface for a smooth user experience.

The chatbot uses advanced language models to ensure polite, accurate, and engaging interactions, optimizing the screening process for diverse tech stacks.

## Installation Instructions

1. **Clone or Download the Repository**: Ensure you have the project files in a local directory.

2. **Install Python**: Make sure Python 3.8 or higher is installed on your system.

3. **Set Up Virtual Environment** (Recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your HuggingFace API token:
     ```
     HUGGINGFACEHUB_API_TOKEN=your_api_token_here
     ```
   - Obtain the token from [HuggingFace](https://huggingface.co/settings/tokens).

6. **Run the Application**:
   ```
   streamlit run app.py
   ```
   - Open the provided URL in your browser to interact with the chatbot.

## Usage Guide

- **Starting the Chat**: The chatbot begins with a greeting and guides you through the screening process step by step.
- **Providing Information**: Respond to prompts for name, email, phone, location, experience, role, and tech stack. The chatbot validates inputs and re-prompts if necessary.
- **Technical Questions**: After gathering details, the chatbot generates and asks 5 tailored technical questions based on your tech stack.
- **Completing the Interview**: Answer the questions, and the session ends with a thank-you message.
- **Navigation**: Use the chat interface to send responses. The app handles the flow automatically.

## Technical Details

- **Libraries Used**:
  - `langchain-core` and `langchain-huggingface`: For building and managing LLM interactions.
  - `pydantic`: For data validation and state management.
  - `streamlit`: For the web-based chat UI.
  - `huggingface-hub`: For accessing HuggingFace models.
  - `python-dotenv`: For loading environment variables.

- **Model Details**: The chatbot uses the Meta Llama-3.1-8B-Instruct model via HuggingFace's API for generating responses and questions.

- **Architectural Decisions**:
  - **LangGraph Workflow**: Manages the conversation flow with nodes for each step (ask/process pairs).
  - **Modular Nodes**: Separate files for each information-gathering stage, promoting maintainability.
  - **State Management**: Uses Pydantic's `GraphState` to track user data and conversation stage.
  - **Validation**: Custom functions ensure data quality (e.g., email regex, name character checks).
  - **UI with Streamlit**: Provides a simple, interactive chat experience without complex frontend development.

## Prompt Design

Prompts were crafted to be clear, concise, and directive, ensuring the LLM produces desired outputs:

- **Information Gathering**: Prompts for name, email, etc., include context about the agency, purpose, and assurances (e.g., privacy for email/phone). This builds trust and guides natural responses.
- **Technical Question Generation**: The `questions_prompt` template takes the tech stack as input and instructs the model to generate 5 challenging, relevant questions. Guidelines handle diversity (e.g., programming languages, frameworks, databases) and ensure appropriate difficulty for screening.
- **Optimization**: Prompts avoid ambiguity, specify formats (e.g., numbered lists), and adapt to broad or specific tech stacks for accurate, engaging content.

## Challenges & Solutions

- **Import Errors**: Relative imports failed initially due to `nodes/` not being a package. Solution: Added `__init__.py` to make it a Python package and updated imports to use relative paths (e.g., `from .name_node import`).
- **PromptTemplate Invocation**: `model.invoke()` rejected `PromptTemplate` objects. Solution: Used `.format()` to convert templates to strings before invocation.
- **Model Loading**: Slow initialization caused timeouts. Solution: Ensured proper API token configuration and handled async loading in the UI.
- **Flow Control in UI**: Automatic graph edges conflicted with user input waits. Solution: Implemented manual state management in Streamlit, calling nodes sequentially based on user responses.
- **Validation and Extraction**: Ensuring accurate data extraction from user inputs. Solution: Used LLM-based extraction prompts for flexibility, combined with regex validations for reliability