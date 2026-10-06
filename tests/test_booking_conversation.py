from langchain_core.messages import HumanMessage
from langgraph.types import Command

from agent.graph import travel_agent


config = {
    "configurable": {
        "thread_id": "booking-conversation-test-1"
    }
}


result = travel_agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Find me a flight from DXB to LHR "
                    "on 2026-10-21 for 1 adult."
                )
            )
        ],
        "approved": False,
    },
    config=config,
)


print("\n--- FLIGHT SEARCH ---")

for message in result["messages"]:
    print("\n--------------------")
    print(type(message).__name__)

    if getattr(message, "tool_calls", None):
        print("TOOL CALLS:")
        print(message.tool_calls)
    else:
        print(message.content)


print("\n\n--- USER SELECTS A FLIGHT ---")


result = travel_agent.invoke(
    {
        "messages": [
            HumanMessage(
                content="Book the first one."
            )
        ]
    },
    config=config,
)


for message in result["messages"]:
    print("\n--------------------")
    print(type(message).__name__)

    if getattr(message, "tool_calls", None):
        print("TOOL CALLS:")
        print(message.tool_calls)
    else:
        print(message.content)


print("\n\n--- USER PROVIDES PASSENGER DETAILS ---")

result = travel_agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Passenger details: "
                    "First name Test, "
                    "last name Traveller, "
                    "date of birth 1990-01-01, "
                    "gender m, "
                    "title Mr, "
                    "email test@example.com, "
                    "phone number +442080160000."
                )
            )
        ]
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

print("\n\n--- USER APPROVES BOOKING ---")

result = travel_agent.invoke(
    Command(resume=True),
    config=config,
)

print("\nRESULT AFTER APPROVAL:")

for message in result["messages"]:
    print("\n--------------------")
    print(type(message).__name__)

    if getattr(message, "tool_calls", None):
        print("TOOL CALLS:")
        print(message.tool_calls)
    else:
        print(message.content)