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


run_test(
    "I want a relaxing destination in Italy."
)

run_test(
    "Suggest a historical destination in Italy."
)

run_test(
    "I want an adventure destination in Switzerland."
)

run_test(
    "Suggest an adventure destination in Italy."
)