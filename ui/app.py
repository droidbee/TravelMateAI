from pathlib import Path
import sys
import streamlit as st
from langchain_core.messages import HumanMessage


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


query = st.text_input(
    "Where would you like to go?",
    placeholder="Example: I want a relaxing destination in Italy.",
)


if st.button("Ask TravelMate"):
    if not query.strip():
        st.warning("Please enter a travel question.")
    else:
        with st.spinner("Finding destinations..."):
            result = travel_agent.invoke(
                {
                    "messages": [
                        HumanMessage(content=query)
                    ]
                }
            )

        final_message = result["messages"][-1]

        st.subheader("TravelMate")
        st.write(final_message.content)