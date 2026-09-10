from crewai import Task
from app.agents import order_agent


def build_order_task(customer_request: str) -> Task:
    return Task(
        description=f"A customer sent this request: '{customer_request}'. "
                     f"Extract the order ID from the request and look up its full details "
                     f"(status, delivery status, product, date, customer email) using your tool.",
        expected_output="The full order details, or a clear statement if no order was found.",
        agent=order_agent
    )