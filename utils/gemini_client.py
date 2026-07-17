import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def _get_api_key():
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
        return "⚠️ Gemini API key not configured."

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(DEFAULT_MODEL)

        if system_instruction:
            prompt = f"{system_instruction}\n\n{prompt}"

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"⚠️ Gemini Error: {str(e)}"


