from langchain_ollama import ChatOllama

from config.settings import (
    CLOUD_OLLAMA_MODEL,
    LLM_MODE,
    LOCAL_OLLAMA_MODEL,
    OLLAMA_API_KEY,
    OLLAMA_CLOUD_URL,
)


def create_llm() -> ChatOllama:
    if LLM_MODE == "cloud":
        if not OLLAMA_API_KEY:
            raise ValueError(
                "OLLAMA_API_KEY is required when LLM_MODE=cloud."
            )

        return ChatOllama(
            model=CLOUD_OLLAMA_MODEL,
            base_url=OLLAMA_CLOUD_URL,
            client_kwargs={
                "headers": {
                    "Authorization": f"Bearer {OLLAMA_API_KEY}"
                }
            },
            temperature=0,
        )

    return ChatOllama(
        model=LOCAL_OLLAMA_MODEL,
        temperature=0,
    )