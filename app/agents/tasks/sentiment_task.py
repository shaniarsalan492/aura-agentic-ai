from crewai import Task
from app.agents import sentiment_agent


def build_sentiment_task(customer_request: str) -> Task:
    return Task(
        description=f"Analyze this customer request for sentiment and urgency: '{customer_request}'. "
                     f"Classify sentiment as positive, neutral, negative, or angry. Classify priority as "
                     f"low, medium, high, or urgent (angry/frustrated tone or repeated complaints = high/urgent). "
                     f"Write a one-sentence summary of the issue. Extract the order ID directly from the "
                     f"customer's message text if mentioned (e.g. 'ORD1052'), and use 'unknown' for customer_id. "
                     f"Then call your ticket creation tool with these details.",
        expected_output="Confirmation that a ticket was created, including sentiment and priority.",
        agent=sentiment_agent
    )