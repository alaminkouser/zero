import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.mcp import MCPToolset
from fastmcp.client import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport

from .tools.current_datetime import current_datetime
from .tools.email_read_unseen import email_read_unseen
from .tools.status_put import status_put

model = GoogleModel(
    "gemma-4-26b-a4b-it",  # "gemma-4-31b-it",
    provider=GoogleProvider(api_key=os.getenv("GOOGLE_API_KEY")),
)

agent = Agent(
    model,
    tools=[current_datetime, email_read_unseen, status_put],
    toolsets=[
        MCPToolset(
            StdioTransport(
                command="npx",
                args=["@bitbonsai/mcpvault", os.getenv("NOTEBOOK_PATH", "")],
            )
        ),
        MCPToolset(
            StdioTransport(
                command="npx",
                args=["@playwright/mcp@latest"],
            )
        ),
        MCPToolset(
            Client(
                StreamableHttpTransport(
                    "https://mcp.serpapi.com/" + os.getenv("SERP_API_KEY", "") + "/mcp"
                )
            )
        ),
    ],
)

app = agent.to_web(html_source="./pydantic-ai-ui.html")
