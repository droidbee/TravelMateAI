import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

from tools.destination_tool import search_destinations


load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")


llm = ChatOllama(
    model="gpt-oss:20b",
    base_url="https://ollama.com",
    client_kwargs={
        "headers": {
            "Authorization": f"Bearer {api_key}"
        }
    },
    temperature=0,
)


llm_with_tools = llm.bind_tools(
    [search_destinations]
)


response = llm_with_tools.invoke(
    "I want a relaxing destination in Italy."
)


print("\nModel response:")
print(response.content)

print("\nTool calls:")
print(response.tool_calls)