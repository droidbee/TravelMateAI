from langchain_core.messages import HumanMessage

from agent.graph import travel_agent


def run_test(query: str):
    print("\n" + "=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    result = travel_agent.invoke(
        {
            "messages": [
                HumanMessage(content=query)
            ]
        }
    )

    for message in result["messages"]:
        print(f"\n{type(message).__name__}:")

        if message.content:
            print(message.content)

        if getattr(message, "tool_calls", None):
            print("Tool calls:")
            print(message.tool_calls)


from langchain_core.messages import HumanMessage


def run_conversation_test():
    print("\n" + "=" * 70)
    print("MULTI-TURN FLIGHT SEARCH")
    print("=" * 70)

    messages = []

    # Turn 1
    first_query = "Find me a flight from DXB to LHR for 1 adult."

    print("\nUSER:")
    print(first_query)

    messages.append(
        HumanMessage(content=first_query)
    )

    result = travel_agent.invoke(
        {"messages": messages}
    )

    first_response = result["messages"][-1]

    print("\nASSISTANT:")
    print(first_response.content)

    # Keep the conversation history returned by the graph.
    messages = result["messages"]

    # Turn 2
    second_query = "October 21, 2026."

    print("\nUSER:")
    print(second_query)

    messages.append(
        HumanMessage(content=second_query)
    )

    result = travel_agent.invoke(
        {"messages": messages}
    )

    print("\n--- Messages produced in turn 2 ---")

    for message in result["messages"][len(messages):]:
        print(f"\n{type(message).__name__}:")

        if message.content:
            print(message.content)

        if getattr(message, "tool_calls", None):
            print("Tool calls:")
            print(message.tool_calls)


# run_test(
#     "Find me a flight from DXB to LHR "
#     "on 2026-10-21 for 1 adult."
# )

# run_test(
#     "Find me a flight from DXB to LHR."
# )

run_conversation_test()