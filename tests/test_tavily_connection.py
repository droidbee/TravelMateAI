import os

import requests
from dotenv import load_dotenv


load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

url = "https://api.tavily.com/search"

payload = {
    "api_key": TAVILY_API_KEY,
    "query": "latest travel news in London",
    "search_depth": "basic",
    "max_results": 5,
}

response = requests.post(
    url,
    json=payload,
    timeout=30,
)

print("Status code:")
print(response.status_code)

data = response.json()

print("\nResponse keys:")
print(data.keys())

print("\nAnswer:")
print(data.get("answer"))

print("\nResults:")

for result in data.get("results", []):
    print("\nTitle:")
    print(result.get("title"))

    print("URL:")
    print(result.get("url"))

    print("Content:")
    print(result.get("content"))