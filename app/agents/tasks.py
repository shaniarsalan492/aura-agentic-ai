from datetime import datetime
from crewai import Task
from app.agents import (
    sentiment_agent, order_agent, rag_agent, decision_agent, communication_agent
)


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


def build_order_task(customer_request: str) -> Task:
    return Task(
        description=f"A customer sent this request: '{customer_request}'. "
                     f"Extract the order ID from the request and look up its full details "
                     f"(status, delivery status, product, date, customer email) using your tool.",
        expected_output="The full order details, or a clear statement if no order was found.",
        agent=order_agent
    )


def build_policy_task(customer_request: str) -> Task:
    return Task(
        description=f"Based on this customer request: '{customer_request}', search company policy "
                     f"ONCE using a single well-formed query covering delivery delays and refund eligibility. "
                     f"Do not repeat searches — one search is sufficient to gather the relevant policy chunks.",
        expected_output="The relevant policy rules that apply to this situation.",
        agent=rag_agent
    )

def build_decision_task(customer_request: str, order_task: Task, policy_task: Task) -> Task:
    return Task(
        description=f"Today's date is {datetime.now().strftime('%Y-%m-%d')}. "
                     f"The original customer request was: '{customer_request}'. "
                     f"Using the order details and the policy rules found so far, determine the correct "
                     f"resolution. IMPORTANT RULES: "
                     f"(a) Calculate the number of days between the order date and today's date to determine "
                     f"if any delay threshold (e.g. 7 business days) has been crossed. Show this calculation. "
                     f"(b) If the customer states the item arrived damaged, defective, or incorrect, treat "
                     f"this claim as valid — the system has no way to independently verify item condition. "
                     f"(c) If a dollar amount is mentioned anywhere in the original customer request, use it "
                     f"to determine if the $50 human-approval threshold applies. "
                     f"(d) If the request does NOT meet any policy criteria for eligibility (e.g., a simple "
                     f"change of mind on an already-delivered item with no damage claim), you must clearly "
                     f"state it is NOT eligible and NOT call the Approval Request Tool — do not invent "
                     f"'exception' or 'special case' approval paths that aren't part of company policy. "
                     f"Only call the tool when the request genuinely meets an eligibility criterion AND "
                     f"crosses the $50 threshold. "
                     f"(e) NEVER call the Approval Request Tool for an order that was not found in the "
                     f"database (i.e. the Order Agent reported 'no order found'). In that case, regardless "
                     f"of any dollar amount mentioned by the customer, simply ask the customer to verify "
                     f"their order ID/details — do not create an approval request or promise a refund for "
                     f"an order that cannot be confirmed to exist. "
                     f"State clearly: (1) eligibility, (2) reasoning, (3) whether human approval is required. "
                     f"If approval is required, you MUST call your Approval Request Tool before finishing.",
        expected_output="A clear decision with reasoning and an approval flag (yes/no).",
        agent=decision_agent,
        context=[order_task, policy_task]
    )


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