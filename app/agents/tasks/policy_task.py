from crewai import Task
from app.agents import rag_agent


def build_policy_task(customer_request: str) -> Task:
    return Task(
        description=f"Based on this customer request: '{customer_request}', search company policy "
                     f"ONCE using a single well-formed query covering delivery delays and refund eligibility. "
                     f"Do not repeat searches — one search is sufficient to gather the relevant policy chunks.",
        expected_output="The relevant policy rules that apply to this situation.",
        agent=rag_agent
    )