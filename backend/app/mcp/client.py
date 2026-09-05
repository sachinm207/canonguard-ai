import json
import logging
from typing import Dict, Any, List, Optional
from ..db.clickhouse import ch_engine

logger = logging.getLogger("canonguard.mcp")

class ClickHouseMCPClient:
    """
    Client for the official ClickHouse MCP Server (mcp-clickhouse).
    Provides standardized tool-calling interfaces for AI agents:
    - execute_query: Parameterized ClickHouse SQL execution
    - find_similar_events: Columnar vector cosine similarity
    - get_lore_invariants: Universal physical and biological laws
    """
    def __init__(self):
        self.server_name = "mcp-clickhouse"

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Returns the MCP tool definitions for LLM tool calling."""
        return [
            {
                "name": "clickhouse_execute_query",
                "description": "Execute a high-speed analytical query against ClickHouse columnar tables.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The parameterized SQL query"},
                        "parameters": {"type": "object", "description": "Named parameters for the query"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "clickhouse_vector_search",
                "description": "Perform cosine distance vector search over canon timeline events in ClickHouse.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query_vector": {"type": "array", "items": {"type": "number"}, "description": "768-dim query embedding"},
                        "top_k": {"type": "integer", "default": 3}
                    },
                    "required": ["query_vector"]
                }
            },
            {
                "name": "clickhouse_get_lore_invariants",
                "description": "Query universe physical, biological, or technological laws.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "BIOLOGY, PHYSICS, MAGIC, TECHNOLOGY"},
                        "entity_or_species": {"type": "string", "description": "Target entity or species"}
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches tool execution directly to the ClickHouse engine."""
        if tool_name == "clickhouse_vector_search":
            results = ch_engine.search_similar_events(
                query_vec=arguments.get("query_vector", []),
                top_k=arguments.get("top_k", 3)
            )
            return {"status": "success", "results": results}
        elif tool_name == "clickhouse_get_lore_invariants":
            results = ch_engine.get_lore_rules(
                category=arguments.get("category"),
                entity_or_species=arguments.get("entity_or_species")
            )
            return {"status": "success", "results": results}
        else:
            return {"status": "error", "message": f"Unknown MCP tool: {tool_name}"}

mcp_client = ClickHouseMCPClient()
