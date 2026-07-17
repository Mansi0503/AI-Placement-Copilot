import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")


def _get_api_key():
    key = None
    try:
        key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass

    if not key:
        key = os.getenv("GEMINI_API_KEY")

    return key


def is_configured():
    return bool(_get_api_key())


def generate(prompt: str, system_instruction: str = None, temperature: float = 0.7):
    if not is_configured():
        return "⚠️ Gemini API key not configured."

    try:
        client = genai.Client(api_key=_get_api_key())

        if system_instruction:
            prompt = f"{system_instruction}\n\n{prompt}"

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
        )

        return response.text

    except Exception as e:
        return f"⚠️ Gemini request failed: {e}"