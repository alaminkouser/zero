import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.mcp import MCPToolset
from fastmcp.client import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport

from .tools.current_datetime import current_datetime
from .tools.email_read_unseen import email_read_unseen
from .tools.status_put import status_put

model = OpenAIChatModel(
    "llama",
    provider=OpenAIProvider(base_url="http://127.0.0.1:8080/v1"),
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
