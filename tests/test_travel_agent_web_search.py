from langchain_core.messages import HumanMessage

from agent.graph import travel_agent


queries = [
    "Suggest relaxing destinations in Italy.",
    "Find a flight from DXB to LHR on October 21, 2026 for one adult.",
    "Are there any current travel disruptions affecting London?",
]


for query in queries:
    print("\n\n======================================")
    print("QUERY:", query)
    print("======================================")

    result = travel_agent.invoke(
        {
            "messages": [
                HumanMessage(content=query)
            ]
        }
    )

    for message in result["messages"]:
        print("\n--------------------")
        print(type(message).__name__)

        if getattr(message, "tool_calls", None):
            print("TOOL CALLS:")
            print(message.tool_calls)

        elif type(message).__name__ == "ToolMessage":
            print("TOOL:")
            print(message.name)

        else:
            print(message.content)