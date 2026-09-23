import os

from dotenv import load_dotenv


load_dotenv()


def get_setting(name: str, default=None):
    value = os.getenv(name)

    if value is not None:
        return value

    try:
        import streamlit as st
        return st.secrets.get(name, default)
    except Exception:
        return default


LLM_MODE = get_setting("LLM_MODE", "local")

OLLAMA_API_KEY = get_setting("OLLAMA_API_KEY")

LOCAL_OLLAMA_MODEL = "llama3.2:3b"
CLOUD_OLLAMA_MODEL = "gpt-oss:20b"

OLLAMA_CLOUD_URL = "https://ollama.com"

DUFFEL_API_URL = "https://api.duffel.com/air/offer_requests"

DUFFEL_ACCESS_TOKEN = get_setting("DUFFEL_ACCESS_TOKEN")