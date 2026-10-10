# llm.py
"""
Generates narration text from narration prompt
"""

# Import libraries
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Constants
MODEL_NAME = "openai/gpt-oss-120b"
load_dotenv()
model = None


def get_llm() -> ChatGroq:
    """Loads the Groq model once and then reuses it"""
    global model

    if model is not None:
        return model

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment. Check .env file.")

    model = ChatGroq(model = MODEL_NAME, api_key = api_key, 
                     reasoning_effort = "medium", temperature = 0.8)

    return model


def generate_narration(prompt: str) -> str:
    """
    Generates narration text

    Catches exceptions from the Groq call (rate limits, network errors,
    etc.), wraps them with context, and re-raises - the original exception
    is chained via `from e` so its type/traceback is preserved
    """
    if not prompt or not prompt.strip():
        raise ValueError("generate_narration() requires a non-empty prompt")

    llm = get_llm()

    try:
        response = llm.invoke(prompt)
    except Exception as e:
        raise RuntimeError(f"Groq narration call failed (model = {MODEL_NAME}): {e}") from e

    return response.content
