from crewai import Agent
from app.agents.llm_config import llm
from app.tools.policy_tools import policy_search_tool

rag_agent = Agent(
    role="Knowledge & Policy Specialist",
    goal="Find and summarize the most relevant company policy information for a given customer situation.",
    backstory="You are an expert at searching company policy documents (delivery, refund, warranty) "
               "and extracting the exact rules that apply to a customer's case.",
    tools=[policy_search_tool],
    llm=llm,
    verbose=True
)