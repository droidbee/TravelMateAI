from typing_extensions import TypedDict

from langgraph.graph import START, END, StateGraph
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import InMemorySaver


class BookingState(TypedDict):
    flight: str
    approved: bool


def prepare_booking(state: BookingState):
    print("\nPreparing booking for:")
    print(state["flight"])

    return {}


def request_approval(state: BookingState):
    approval = interrupt(
        {
            "question": "Do you want to confirm this booking?",
            "flight": state["flight"],
        }
    )

    return {
        "approved": approval
    }


def complete_booking(state: BookingState):
    if state["approved"]:
        print("\nBooking confirmed.")
    else:
        print("\nBooking cancelled.")

    return {}


builder = StateGraph(BookingState)

builder.add_node("prepare_booking", prepare_booking)
builder.add_node("request_approval", request_approval)
builder.add_node("complete_booking", complete_booking)

builder.add_edge(START, "prepare_booking")
builder.add_edge("prepare_booking", "request_approval")
builder.add_edge("request_approval", "complete_booking")
builder.add_edge("complete_booking", END)

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)

config = {
    "configurable": {
        "thread_id": "booking-test-1"
    }
}

result = graph.invoke(
    {
        "flight": "Iberia IB3177 - DXB to LHR - $214.59",
        "approved": False,
    },
    config=config,
)

print("\nGraph result:")
print(result)

print("\n--- Human approves booking ---")

result = graph.invoke(
    Command(resume=True),
    config=config,
)

print("\nResumed graph result:")
print(result)