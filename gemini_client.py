"""Thin wrapper around the Gemini API.

If no API key is configured, `is_configured()` returns False and every page
in the app falls back to a rule-based / templated response so the project
still runs end-to-end for a demo without billing setup.
"""

import os
import streamlit as st

try:
    import google.generativeai as genai
except ImportError:  # library not installed yet
    genai = None

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def _get_api_key():
    # Prefer Streamlit secrets (used on Streamlit Community Cloud),
    # fall back to a local .env / environment variable.
    key = None
    try:
        key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        key = None
    if not key:
        key = os.environ.get("GEMINI_API_KEY")
    return key


def is_configured():
    return bool(_get_api_key()) and genai is not None


@st.cache_resource(show_spinner=False)
def _get_model(model_name=DEFAULT_MODEL):
    api_key = _get_api_key()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)


def generate(prompt: str, system_instruction: str = None, temperature: float = 0.7) -> str:
    """Return generated text, or a clear error string if the call fails."""
    if not is_configured():
        return (
            "⚠️ Gemini API key not configured. Add GEMINI_API_KEY to your .env file "
            "(or Streamlit secrets) to enable AI-generated responses. "
            "Showing a basic fallback instead."
        )
    try:
        model = _get_model()
        if system_instruction:
            full_prompt = f"{system_instruction}\n\n{prompt}"
        else:
            full_prompt = prompt
        response = model.generate_content(
            full_prompt,
            generation_config={"temperature": temperature},
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini request failed: {e}"
