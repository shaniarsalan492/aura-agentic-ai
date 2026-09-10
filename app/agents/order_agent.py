from crewai import Agent
from app.agents.llm_config import llm
from app.tools.order_tools import order_lookup_tool

order_agent = Agent(
    role="Order Investigation Specialist",
    goal="Retrieve accurate order details from the business database to support decision-making.",
    backstory="You are an expert at looking up customer orders and reporting their exact status, "
               "delivery information, and history without making assumptions.",
    tools=[order_lookup_tool],
    llm=llm,
    verbose=True
)