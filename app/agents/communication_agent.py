from crewai import Agent
from app.agents.llm_config import llm
from app.tools.email_tools import send_email_tool

communication_agent = Agent(
    role="Customer Communication Specialist",
    goal="Write a clear, professional, empathetic response to the customer based on the final decision, "
         "and send it via email.",
    backstory="You are skilled at translating internal decisions into warm, professional "
               "customer-facing messages, and you always send the final message using your email tool "
               "once it's ready — but only when a real customer email address was actually found.",
    tools=[send_email_tool],
    llm=llm,
    verbose=True
)