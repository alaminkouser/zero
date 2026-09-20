# Zero Agent Demo

## Overview

This repository contains a **Zero** demo application built with **Pydantic AI** and **FastMCP**. The app showcases how to create a language model‑driven agent, expose it as a web UI, and integrate multiple toolsets:

- **Current date/time** utility
- **Email fetching** (unseen emails)
- **Status updates** via a custom HTTP endpoint
- **MCP (Modular Compute Platform)** integrations for Vault, Playwright, SerpAPI, and Firecrawl.

The agent is powered by an OpenAI‑compatible LLaMA model running locally via `http://127.0.0.1:8080/v1`.

## Project Structure

```
.
├── .envrc                 # Environment variable helpers (direnv)
├── .gitignore
├── app
│   ├── main.py            # Entry point – builds the agent and launches the UI
│   └── tools
│       ├── current_datetime.py   # Returns the current datetime
│       ├── email_read_unseen.py  # Reads unseen emails
│       └── status_put.py         # Sends a status payload to a remote service
├── pydantic-ai-ui.html   # Front‑end HTML for the interactive UI
├── requirements.txt       # Python dependencies
└── README.md              # **You are reading it right now**
```

## Prerequisites

- **Python 3.9+**
- **Node.js** (required for the `npx`‑based MCP tools)
- **Docker** (optional, for running the LLaMA inference server)
- Environment variables (set via `direnv` or manually):
  - `NOTEBOOK_PATH` – Path for the MCP Vault tool
  - `SERP_API_KEY` – API key for SerpAPI integration
  - `FIRECRAWL_API_KEY` – API key for Firecrawl integration

## Installation

```bash
# Clone the repository
git clone https://github.com/alaminkouser/zero.git
cd zero

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

Make sure the required environment variables are exported before running the app.

## Running the Application

```bash
# Activate the virtual environment if not already active
source .venv/bin/activate

# Start the agent UI (this will launch a local web server)
python -m app.main
```

Open your browser and navigate to the URL printed by the script (by default `http://127.0.0.1:8000`). You will see an interactive chat interface powered by the LLaMA model.

## Adding Custom Tools

To extend the agent, add a new module under `app/tools/` that follows the signature expected by **Pydantic AI** (a callable with a docstring describing its purpose). Then import the tool in `app/main.py` and include it in the `tools=` list when constructing the `Agent`.


