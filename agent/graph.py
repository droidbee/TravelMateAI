

import json
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END
from langgraph.graph.state import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt
from agent.prompts import TRAVEL_AGENT_SYSTEM_PROMPT
from agent.state import TravelAgentState
from tools.booking_tool import book_flight
from tools.web_search_tool import search_web
from llm.llm_client import create_llm
from tools.destination_tool import search_destinations
from tools.flight_tool import search_flights


read_tools = [search_destinations, search_flights,search_web]

all_tools = [*read_tools,book_flight]

llm = create_llm()
llm_with_tools = llm.bind_tools(
        all_tools
    )

def agent_node(state: TravelAgentState) -> TravelAgentState:

    messages = [SystemMessage(content=TRAVEL_AGENT_SYSTEM_PROMPT) ,*state["messages"]]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tools_node = ToolNode(read_tools)

PASSENGER_FIELDS = [
    "given_name",
    "family_name",
    "born_on",
    "gender",
    "title",
    "email",
    "phone_number",
]


def validate_booking_node(state: TravelAgentState):
    """
    Validate that passenger details in the proposed book_flight
    call actually came from the user.

    We do not trust the LLM to invent or infer passenger details.
    """

    last_ai_message = next(
        message
        for message in reversed(state["messages"])
        if isinstance(message, AIMessage)
        and getattr(message, "tool_calls", None)
    )

    booking_call = next(
        tool_call
        for tool_call in last_ai_message.tool_calls
        if tool_call["name"] == "book_flight"
    )

    booking_args = booking_call["args"]

    user_text = " ".join(
        message.content
        for message in state["messages"]
        if isinstance(message, HumanMessage)
        and isinstance(message.content, str)
    ).lower()

    missing_or_unverified = []

    for field in PASSENGER_FIELDS:
        value = booking_args.get(field)

        if not value:
            missing_or_unverified.append(field)
            continue

        if str(value).lower() not in user_text:
            missing_or_unverified.append(field)

    return {
        "booking_valid": len(missing_or_unverified) == 0,
        "missing_booking_fields": missing_or_unverified,
    }

def route_agent(state: TravelAgentState):
    last_message = state["messages"][-1]

    if not last_message.tool_calls:
        return "end"

    tool_names = [
        tool_call["name"]
        for tool_call in last_message.tool_calls
    ]

    if "book_flight" in tool_names:
        return "validate_booking"

    return "tools"

def route_booking_validation(state: TravelAgentState):
    if state["booking_valid"]:
        return "approval"

    return "invalid"

def invalid_booking_node(state: TravelAgentState):
    fields = state["missing_booking_fields"]

    field_names = ", ".join(
        field.replace("_", " ")
        for field in fields
    )

    return {
        "messages": [
            AIMessage(
                content=(
                    "I still need passenger information directly "
                    "from you before I can prepare this booking. "
                    f"Please provide: {field_names}."
                )
            )
        ]
    }

def approval_node(state: TravelAgentState):
    last_message = state["messages"][-1]

    booking_call = next(
        tool_call
        for tool_call in last_message.tool_calls
        if tool_call["name"] == "book_flight"
    )

    booking_args = booking_call["args"]

    flight = find_selected_flight(
        state,
        booking_args["offer_id"],
    )

    approval_request = {
        "question": "Do you want to confirm this test flight booking?",
        "passenger": {
            "name": (
                f"{booking_args['given_name']} "
                f"{booking_args['family_name']}"
            ),
        },
        "price": {
            "amount": booking_args["amount"],
            "currency": booking_args["currency"],
        },
    }

    if flight:
        approval_request["flight"] = {
            "airline": flight["airline"],
            "flight_number": flight["flight_number"],
            "origin": flight["origin"],
            "destination": flight["destination"],
            "departure": flight["departure"],
            "arrival": flight["arrival"],
            "duration": flight["duration"],
            "stops": flight["stops"],
        }

    approved = interrupt(approval_request)

    return {
        "approved": approved
    }

def booking_node(state: TravelAgentState):
    last_ai_message = next(
        message
        for message in reversed(state["messages"])
        if getattr(message, "tool_calls", None)
    )

    booking_call = next(
        tool_call
        for tool_call in last_ai_message.tool_calls
        if tool_call["name"] == "book_flight"
    )

    result = book_flight.invoke(
        booking_call["args"]
    )

    return {
        "messages": [
            ToolMessage(
                content=str(result),
                name="book_flight",
                tool_call_id=booking_call["id"],
            )
        ]
    }

def route_approval(state: TravelAgentState):
    if state["approved"]:
        return "booking"

    return "cancel"

def cancel_booking_node(state: TravelAgentState):
    last_ai_message = next(
        message
        for message in reversed(state["messages"])
        if getattr(message, "tool_calls", None)
    )

    booking_call = next(
        tool_call
        for tool_call in last_ai_message.tool_calls
        if tool_call["name"] == "book_flight"
    )

    result = {
        "success": False,
        "approved": False,
        "booking_created": False,
        "message": "The user declined the booking. No booking was made.",
    }

    return {
        "messages": [
            ToolMessage(
                content=json.dumps(result),
                name="book_flight",
                tool_call_id=booking_call["id"],
            )
        ]
    }

def find_selected_flight(
    state: TravelAgentState,
    offer_id: str,
) -> dict | None:

    for message in reversed(state["messages"]):

        if not isinstance(message, ToolMessage):
            continue

        if message.name != "search_flights":
            continue

        try:
            result = json.loads(message.content)
        except (json.JSONDecodeError, TypeError):
            continue

        for flight in result.get("flights", []):
            if flight.get("offer_id") == offer_id:
                return flight

    return None

graph_builder = StateGraph(TravelAgentState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tools_node)
graph_builder.add_node("approval", approval_node)
graph_builder.add_node("booking", booking_node)
graph_builder.add_node("cancel_booking", cancel_booking_node)
graph_builder.add_node("validate_booking", validate_booking_node)
graph_builder.add_node("invalid_booking", invalid_booking_node)


graph_builder.set_entry_point("agent")

graph_builder.add_conditional_edges(
    "agent",
    route_agent,
    {
        "tools": "tools",
        "validate_booking": "validate_booking",
        "end" :END,
    }
)

graph_builder.add_conditional_edges(
    "validate_booking",
    route_booking_validation,
    {
        "approval": "approval",
        "invalid": "invalid_booking",
    },
)

graph_builder.add_conditional_edges(
    "approval",
    route_approval,
    {
        "booking": "booking",
        "cancel": "cancel_booking",
    }
)

graph_builder.add_edge("tools", "agent")
graph_builder.add_edge("booking", "agent")
graph_builder.add_edge("cancel_booking", "agent")
graph_builder.add_edge(
    "invalid_booking",
    END,
)

checkpointer=InMemorySaver()

travel_agent = graph_builder.compile(checkpointer=checkpointer)