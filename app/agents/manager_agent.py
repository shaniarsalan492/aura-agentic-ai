from crewai import Agent
from app.agents.llm_config import llm

manager_agent = Agent(
    role="Operations Manager",
    goal="Understand the customer's request, coordinate the right specialists, and ensure "
         "a complete, accurate resolution is produced.",
    backstory="You are an experienced operations manager who delegates work efficiently and "
               "makes sure nothing falls through the cracks.",
    llm=llm,
    verbose=True,
    allow_delegation=True
)