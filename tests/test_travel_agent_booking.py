from langchain_core.messages import HumanMessage
from langgraph.types import Command

from agent.graph import travel_agent


config = {
    "configurable": {
        "thread_id": "travel-booking-test-1"
    }
}


query = """
Book flight offer off_test_123 for me.
"""


result = travel_agent.invoke(
    {
        "messages": [
            HumanMessage(content=query)
        ],
        "approved": False,
    },
    config=config,
)


print("\nRESULT:")
print(result)

print("\nMESSAGES:")

for message in result["messages"]:
    print("\n--------------------")
    print(type(message).__name__)

    if getattr(message, "tool_calls", None):
        print("TOOL CALLS:")
        print(message.tool_calls)
    else:
        print(message.content)


print("\nINTERRUPT:")
print(result.get("__interrupt__"))

print("\n--- HUMAN APPROVES ---")

resumed_result = travel_agent.invoke(
    Command(resume=True),
    config=config,
)

print("\nRESUMED RESULT:")

for message in resumed_result["messages"]:
    print("\n--------------------")
    print(type(message).__name__)

    if getattr(message, "tool_calls", None):
        print("TOOL CALLS:")
        print(message.tool_calls)
    else:
        print(message.content)