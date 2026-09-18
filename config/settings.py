import os

from dotenv import load_dotenv


load_dotenv()


LLM_MODE = os.getenv("LLM_MODE", "local")

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

LOCAL_OLLAMA_MODEL = "llama3.2:3b"
CLOUD_OLLAMA_MODEL = "gpt-oss:20b"

OLLAMA_CLOUD_URL = "https://ollama.com"