from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)

response = llm.invoke(
    "What is a good destination in Italy for a relaxing vacation?"
)

print("\nResponse:")
print(response.content)