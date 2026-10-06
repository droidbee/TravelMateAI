import sys
import uuid
from pathlib import Path

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Command


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from agent.graph import travel_agent


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
)

st.title("✈️ TravelMate AI")
st.caption("Your AI travel planning assistant")


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

# Messages shown in the Streamlit UI.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Full LangGraph conversation history.
# This includes HumanMessage, AIMessage tool calls,
# ToolMessages, etc.
if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []

# LangGraph checkpoint thread.
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Stores the HITL approval payload while the graph
# is paused at interrupt().
if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None


config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.header("TravelMate")

    if st.button(
        "➕ New conversation",
        use_container_width=True,
    ):
        # Clear visible UI history.
        st.session_state.messages = []

        # Clear full agent history.
        st.session_state.agent_messages = []

        # A new conversation must use a new LangGraph thread.
        st.session_state.thread_id = str(uuid.uuid4())

        # Remove any pending booking approval.
        st.session_state.pending_approval = None

        st.rerun()


# ---------------------------------------------------------
# Display previous conversation
# ---------------------------------------------------------

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

query = st.chat_input(
    "Ask TravelMate about your next trip...",
    disabled=st.session_state.pending_approval is not None,
)


# ---------------------------------------------------------
# Process normal user message
# ---------------------------------------------------------

if query:

    user_message = HumanMessage(content=query)

    # UI history
    st.session_state.messages.append(user_message)

    # Full agent history
    st.session_state.agent_messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):

        with st.spinner("Planning your trip..."):

            result = travel_agent.invoke(
                {
                    "messages": st.session_state.agent_messages
                },
                config=config,
            )

    # Always preserve the full graph state returned by LangGraph.
    st.session_state.agent_messages = result["messages"]

    # -----------------------------------------------------
    # Did LangGraph pause for human approval?
    # -----------------------------------------------------

    interrupts = result.get("__interrupt__", [])

    if interrupts:

        st.session_state.pending_approval = (
            interrupts[0].value
        )

        # We intentionally do not add another assistant
        # chat message here. The approval card represents
        # the graph's current response.
        st.rerun()

    else:

        # Normal agent response.
        final_message = result["messages"][-1]

        st.session_state.messages.append(
            AIMessage(
                content=final_message.content
            )
        )

        st.rerun()


# ---------------------------------------------------------
# Human-in-the-loop booking approval
# ---------------------------------------------------------
#
# IMPORTANT:
# This must be OUTSIDE `if query:`.
#
# Streamlit reruns the whole script after an interrupt.
# On that rerun `query` is None, but pending_approval
# remains in session_state.
# ---------------------------------------------------------

approval = st.session_state.pending_approval

if approval:

    st.divider()

    st.subheader("✈️ Confirm test booking")

    flight = approval.get("flight", {})
    passenger = approval.get("passenger", {})
    price = approval.get("price", {})

    st.write(
        f"**Flight:** "
        f"{flight.get('airline', 'Unknown')} "
        f"{flight.get('flight_number', '')}"
    )

    st.write(
        f"**Route:** "
        f"{flight.get('origin', 'Unknown')} → "
        f"{flight.get('destination', 'Unknown')}"
    )

    st.write(
        f"**Departure:** "
        f"{flight.get('departure', 'Unknown')}"
    )

    st.write(
        f"**Arrival:** "
        f"{flight.get('arrival', 'Unknown')}"
    )

    st.write(
        f"**Duration:** "
        f"{flight.get('duration', 'Unknown')}"
    )

    st.write(
        f"**Stops:** "
        f"{flight.get('stops', 'Unknown')}"
    )

    st.write(
        f"**Passenger:** "
        f"{passenger.get('name', 'Unknown')}"
    )

    st.write(
        f"**Price:** "
        f"{price.get('currency', '')} "
        f"{price.get('amount', '')}"
    )

    st.warning(
        "This is a test booking in the Duffel test environment. "
        "No real payment will be made."
    )

    confirm_col, cancel_col = st.columns(2)

    # -----------------------------------------------------
    # Confirm booking
    # -----------------------------------------------------

    with confirm_col:

        confirm_booking = st.button(
            "Confirm booking",
            type="primary",
            use_container_width=True,
        )

    # -----------------------------------------------------
    # Cancel booking
    # -----------------------------------------------------

    with cancel_col:

        cancel_booking = st.button(
            "Cancel",
            use_container_width=True,
        )

    # -----------------------------------------------------
    # User APPROVES
    # -----------------------------------------------------

    if confirm_booking:

        with st.spinner("Creating test booking..."):

            result = travel_agent.invoke(
                Command(resume=True),
                config=config,
            )

        # Save complete LangGraph history.
        st.session_state.agent_messages = (
            result["messages"]
        )

        # Booking node returns to the agent, so the last
        # message should be the grounded assistant response.
        final_message = result["messages"][-1]

        st.session_state.messages.append(
            AIMessage(
                content=final_message.content
            )
        )

        # Approval is now completed.
        st.session_state.pending_approval = None

        st.rerun()

    # -----------------------------------------------------
    # User REJECTS
    # -----------------------------------------------------

    if cancel_booking:

        with st.spinner("Cancelling booking..."):

            result = travel_agent.invoke(
                Command(resume=False),
                config=config,
            )

        # Save complete LangGraph history.
        st.session_state.agent_messages = (
            result["messages"]
        )

        # cancel_booking_node -> agent should produce
        # the final user-facing cancellation response.
        final_message = result["messages"][-1]

        st.session_state.messages.append(
            AIMessage(
                content=final_message.content
            )
        )

        # Remove approval card.
        st.session_state.pending_approval = None

        st.rerun()