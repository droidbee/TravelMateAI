# TravelMate AI

An AI travel planning assistant that recommends destinations from local data. Users ask in natural language (for example, “I want a relaxing destination in Italy”), a LangGraph agent calls a destination search tool, and Streamlit shows the reply.

Recommendations come only from `data/destinations.json`. The model does not invent places that are not in that catalog.

## Features

- Natural-language destination search by country and interest
- LangGraph agent with Ollama tool calling (`llama3.2:3b`)
- Local destination catalog (Italy, Spain, Switzerland)
- Streamlit UI for asking questions and reading recommendations
- Unit tests for the destination tool, plus scripts to try the LLM and full agent

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) running locally
- The `llama3.2:3b` model:

```bash
ollama pull llama3.2:3b
```

## Setup

```bash
python -m venv .venv
```

Activate the virtual environment:

- Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
- macOS / Linux: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
```

Run commands from the project root so Python can import `agent`, `tools`, `models`, and `llm`. If imports fail with `ModuleNotFoundError`, set `PYTHONPATH` to the project root:

```powershell
$env:PYTHONPATH = "E:\AI Projects\TravelMateAI"
```

```bash
export PYTHONPATH="$(pwd)"
```

## Run the app

```bash
streamlit run ui/app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`), enter a travel question, and click **Ask TravelMate**.

Example queries:

- I want a relaxing destination in Italy.
- Suggest a historical destination in Italy.
- I want an adventure destination in Switzerland.
- Suggest an adventure destination in Italy.

## Project structure

```
TravelMateAI/
├── agent/                 # LangGraph agent, state, and system prompt
├── tools/                 # Destination search tool
├── models/                # Pydantic schemas
├── llm/                   # Ollama chat client
├── data/                  # Destination catalog (JSON)
├── ui/                    # Streamlit app
├── tests/                 # Tool tests and agent/LLM scripts
├── config/                # Settings placeholder
├── requirements.txt
└── README.md
```

## How it works

1. The Streamlit app sends the user query into the compiled LangGraph graph.
2. The agent node prepends the TravelMate system prompt and asks Ollama whether to call `search_destinations`.
3. If the model requests a tool, `ToolNode` runs the search against `data/destinations.json`.
4. The agent replies using only the tool results (or says nothing matched).

## Tests

Destination tool tests (pytest):

```bash
python -m pytest tests/test_destination_tool.py
```

Ollama connectivity:

```bash
python tests/test_ollama_connection.py
```

Tool calling:

```bash
python tests/test_ollama_tool_calling.py
```

Full travel agent (requires Ollama):

```bash
python tests/test_travel_agent.py
```

## Tech stack

- [LangGraph](https://langchain-ai.github.io/langgraph/) and [LangChain](https://python.langchain.com/)
- [Ollama](https://ollama.com/) via `langchain-ollama`
- [Streamlit](https://streamlit.io/)
- [Pydantic](https://docs.pydantic.dev/)
- [pytest](https://docs.pytest.org/)
