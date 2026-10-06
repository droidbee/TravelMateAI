from langchain_core.messages import HumanMessage

from agent.graph import travel_agent


query = """
I'm planning to travel from DXB to London on October 21, 2026
for one adult.

Find me a flight from DXB to LHR and also check if there are
any current travel disruptions affecting London.
"""


result = travel_agent.invoke(
    {
        "messages": [
            HumanMessage(content=query)
        ]
    },
     config={
        "configurable": {
            "thread_id": "multi-tool-test-1"
        }
    }
)


print("\nQUERY:")
print(query)

print("\nMESSAGES:")

for message in result["messages"]:
    print("\n--------------------")
    print(type(message).__name__)

    if getattr(message, "tool_calls", None):
        print("TOOL CALLS:")
        print(message.tool_calls)

    elif type(message).__name__ == "ToolMessage":
        print("TOOL:")
        print(message.name)
        print("CONTENT:")
        print(message.content)

    else:
        print(message.content)