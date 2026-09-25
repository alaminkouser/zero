import os
from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.mcp import MCPToolset
from fastmcp.client import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport

from .tools.current_datetime import current_datetime
from .tools.email_read_unseen import email_read_unseen
from .tools.status_put import status_put

model = OpenRouterModel(
    "openrouter/free",
    provider=OpenRouterProvider(api_key=os.getenv("OPENROUTER_API_KEY", "")),
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
        MCPToolset(
            Client(
                StreamableHttpTransport(
                    "https://mcp.firecrawl.dev/" + os.getenv("FIRECRAWL_API_KEY", "") + "/v2/mcp"
                )
            )
        ),
    ],
)
