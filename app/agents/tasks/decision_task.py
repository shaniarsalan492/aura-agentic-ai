from datetime import datetime
from crewai import Task
from app.agents import decision_agent


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