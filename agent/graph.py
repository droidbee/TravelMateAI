

from langchain_core.messages import SystemMessage
from langgraph.constants import END
from langgraph.graph.state import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from agent.prompts import TRAVEL_AGENT_SYSTEM_PROMPT
from agent.state import TravelAgentState
from llm.llm_client import create_llm_client
from tools.destination_tool import search_destinations


tools = [search_destinations]

llm = create_llm_client()
llm_with_tools = llm.bind_tools(
        tools
    )

def agent_node(state: TravelAgentState) -> TravelAgentState:

    messages = [SystemMessage(content=TRAVEL_AGENT_SYSTEM_PROMPT) ,*state["messages"]]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tools_node = ToolNode(tools)

graph_builder = StateGraph(TravelAgentState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tools_node)

graph_builder.set_entry_point("agent")

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        "__end__" :END,
    }
)

graph_builder.add_edge("tools", "agent")

travel_agent = graph_builder.compile()