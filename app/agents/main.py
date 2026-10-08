import os
from pydantic_ai import Agent
from pydantic_ai.capabilities import LocalWorkspace
from pydantic_ai_harness import Memory
from pydantic_ai_harness.memory import InMemoryStore
from pydantic_ai_harness import Skills
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.mcp import MCPToolset
from fastmcp.client import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport
from jinja2 import Environment, FileSystemLoader
import yaml

from tools.current_datetime import current_datetime
from tools.email_read_unseen import email_read_unseen
from tools.status_put import status_put



def agent() -> Agent:
    config_file = open("config.yaml", "r", encoding="utf-8")
    config = yaml.safe_load(config_file)
    config_file.close()
    template_env = Environment(loader=FileSystemLoader("app/templates"))

    instructions = template_env.get_template("instructions.j2").render(config=config)
    return Agent(
        OpenRouterModel(
            "openrouter/free",
            provider=OpenRouterProvider(api_key=os.getenv("OPENROUTER_API_KEY", "")),
        ),
        capabilities=[
            LocalWorkspace("."),
            Memory(InMemoryStore()),
            Skills("app/skills"),
        ],
        tools=[current_datetime, email_read_unseen, status_put],
        toolsets=[
            MCPToolset(
                StdioTransport(
                    command="npx",
                    args=["-y", "@bitbonsai/mcpvault", os.getenv("NOTEBOOK_PATH", "")],
                ),
            ).prefixed("notebook"),
            MCPToolset(
                StdioTransport(
                    command="npx",
                    args=["-y", "@sylphx/citra"],
                ),
            ).prefixed("citra"),
            MCPToolset(
                StdioTransport(
                    command="npx",
                    args=["-y", "@playwright/mcp@latest"],
                )
            ).prefixed("playwright"),
            MCPToolset(
                Client(
                    StreamableHttpTransport(
                        "https://mcp.serpapi.com/"
                        + os.getenv("SERP_API_KEY", "")
                        + "/mcp"
                    )
                )
            ).prefixed("serpapi"),
            MCPToolset(
                Client(
                    StreamableHttpTransport(
                        "https://mcp.firecrawl.dev/"
                        + os.getenv("FIRECRAWL_API_KEY", "")
                        + "/v2/mcp"
                    )
                )
            ).prefixed("firecrawl"),
        ],
        instructions=instructions,
    )
