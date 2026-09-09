from crewai.tools import tool
from app.knowledge_base.vectorstore import search_policy


@tool("Policy Search Tool")
def policy_search_tool(query: str) -> str:
    """Searches company policies (delivery, refund, warranty) for relevant information.
    Input should be a natural language question about policy."""
    return search_policy(query)