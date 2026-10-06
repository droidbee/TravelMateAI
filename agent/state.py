from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class TravelAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    approved:bool
    booking_valid: bool
    missing_booking_fields: list[str]