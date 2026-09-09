from crewai import Agent, LLM
from app.config.settings import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from app.tools.order_tools import order_lookup_tool
from app.tools.policy_tools import policy_search_tool
from app.tools.approval_tools import create_approval_request
from app.tools.ticket_tools import create_ticket_tool
from app.tools.email_tools import send_email_tool

llm = LLM(
    model=LLM_MODEL,
    api_key=GOOGLE_API_KEY,
    temperature=LLM_TEMPERATURE
)

sentiment_agent = Agent(
    role="Sentiment & Escalation Analyst",
    goal="Analyze the emotional tone of customer requests and create a support ticket "
         "for every request, flagging urgent/negative cases for faster attention.",
    backstory="You are skilled at reading between the lines of customer messages to detect "
               "frustration, anger, or urgency, and you always log a ticket so nothing falls "
               "through the cracks — even calm requests get a low-priority ticket for record-keeping.",
    tools=[create_ticket_tool],
    llm=llm,
    verbose=True
)

order_agent = Agent(
    role="Order Investigation Specialist",
    goal="Retrieve accurate order details from the business database to support decision-making.",
    backstory="You are an expert at looking up customer orders and reporting their exact status, "
               "delivery information, and history without making assumptions.",
    tools=[order_lookup_tool],
    llm=llm,
    verbose=True
)

rag_agent = Agent(
    role="Knowledge & Policy Specialist",
    goal="Find and summarize the most relevant company policy information for a given customer situation.",
    backstory="You are an expert at searching company policy documents (delivery, refund, warranty) "
               "and extracting the exact rules that apply to a customer's case.",
    tools=[policy_search_tool],
    llm=llm,
    verbose=True
)

decision_agent = Agent(
    role="Decision & Eligibility Analyst",
    goal="Combine order data and policy information to determine the correct resolution "
         "(e.g., refund eligible, not eligible, requires human approval), and create an "
         "approval request in the system whenever one is required.",
    backstory="You are a careful analyst who cross-references order facts with company policy "
               "to reach a fair, policy-compliant decision. Whenever a refund of $50 or more "
               "is involved (or you cannot confirm it's under $50), you MUST call your approval "
               "tool to log a pending approval before finishing your answer.",
    tools=[create_approval_request],
    llm=llm,
    verbose=True
)

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