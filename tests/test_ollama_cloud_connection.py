import os

from dotenv import load_dotenv
from ollama import Client


load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")

client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": f"Bearer {api_key}"
    },
)

response = client.chat(
    model="gpt-oss:20b",
    messages=[
        {
            "role": "user",
            "content": "Suggest one relaxing destination in Italy."
        }
    ],
)

print("\nCloud response:")
print(response["message"]["content"])