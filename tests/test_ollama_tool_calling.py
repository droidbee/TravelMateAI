from langchain_ollama import ChatOllama

from tools.destination_tool import search_destinations


llm = ChatOllama(
    model="llama3.2:3b",
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

if response.tool_calls:
    tool_call = response.tool_calls[0]
    tool_name = tool_call["name"]
    tool_result = search_destinations.invoke(tool_call["args"])

    print("\nTool result:")
    print(tool_result)