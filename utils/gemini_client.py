import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables (.env for local development)
load_dotenv()

# Default Gemini model
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")


def _get_api_key():
    """
    Get API key from Streamlit Secrets first,
    then from local .env file.
    """
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY")


def is_configured():
    return bool(_get_api_key())


def generate(prompt: str, system_instruction: str = None, temperature: float = 0.7):
    api_key = _get_api_key()

    if not api_key:
        return "⚠️ Gemini API key not found. Please configure GEMINI_API_KEY."

    try:
        client = genai.Client(api_key=api_key)

        if system_instruction:
            prompt = f"{system_instruction}\n\n{prompt}"

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
        )

        if hasattr(response, "text") and response.text:
            return response.text

        return "⚠️ No response received from Gemini."

    except Exception as e:
        error = str(e)

        if "404" in error:
            return (
                "⚠️ Selected Gemini model is unavailable.\n"
                "Try changing GEMINI_MODEL to a supported model such as "
                "'gemini-2.5-flash-lite' or another model available to your account."
            )

        if "401" in error or "API_KEY" in error:
            return "⚠️ Invalid Gemini API key."

        return f"⚠️ Gemini Error: {error}"


