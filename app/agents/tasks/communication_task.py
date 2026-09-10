from crewai import Task
from app.agents import communication_agent


def build_communication_task(order_task: Task, decision_task: Task) -> Task:
    return Task(
        description="Using the order details (if any were found) and the final decision/answer, write a "
                     "professional, empathetic response to the customer. "
                     "IMPORTANT: Only use your Send Email Tool if a REAL customer email address was found "
                     "in the order lookup results. If no order was found, no order ID was mentioned, or no "
                     "real email is available, DO NOT call the Send Email Tool — never invent or guess an "
                     "email address. In that case, simply provide the written response without sending.",
        expected_output="The customer response, and confirmation of whether an email was actually sent.",
        agent=communication_agent,
        context=[order_task, decision_task]
    )