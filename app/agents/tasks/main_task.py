from datetime import datetime
from crewai import Task


def build_main_task(customer_request: str) -> Task:
    return Task(
        description=f"Today's date is {datetime.now().strftime('%Y-%m-%d')}. "
                     f"Handle this customer request end-to-end: '{customer_request}'. "
                     f"Delegate to your specialist agents as needed: look up any order details "
                     f"mentioned, search company policy for applicable rules, determine the correct "
                     f"resolution, and produce a final professional customer-facing email as your output.",
        expected_output="A complete, ready-to-send customer email that reflects a policy-correct decision.",
        agent=None
    )