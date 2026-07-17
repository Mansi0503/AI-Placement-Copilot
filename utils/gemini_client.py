import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _get_api_key():
    # First try Streamlit Secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # Then try local .env
    return os.getenv("GEMINI_API_KEY")


def is_configured():
    return _get_api_key() is not None


def generate(prompt: str, system_instruction: str = None, temperature: float = 0.7):
    api_key = _get_api_key()

    if not api_key:
        return "⚠️ GEMINI_API_KEY not found."

    try:
        client = genai.Client(api_key=api_key)

        if system_instruction:
            prompt = f"{system_instruction}\n\n{prompt}"

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
        )

        return response.text

    except Exception as e:
        return f"⚠️ Gemini Error: {str(e)}"


