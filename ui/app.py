import sys
from pathlib import Path

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from agent.graph import travel_agent


st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
)

st.title("✈️ TravelMate AI")
st.caption("Your AI travel planning assistant")


# Create conversation history for this browser session.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Start a new conversation.
with st.sidebar:
    st.header("TravelMate")

    if st.button("➕ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# Display previous conversation.
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)


# Chat input.
query = st.chat_input(
    "Ask TravelMate about your next trip..."
)


if query:
    # Add and display the user's new message.
    user_message = HumanMessage(content=query)
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(query)


    # Give the agent the entire conversation.
    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):

            result = travel_agent.invoke(
                {
                    "messages": st.session_state.messages
                }
            )

            final_message = result["messages"][-1]

            st.markdown(final_message.content)


    # Store only the final assistant response.
    st.session_state.messages.append(
        AIMessage(content=final_message.content)
    )