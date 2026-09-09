# AURA — Autonomous Unified Response & Operations

An intelligent multi-agent AI business operations system built with CrewAI, Gemini, RAG, and Streamlit.

## Overview

AURA automates customer support operations (order inquiries, refunds, warranty questions) using a team of specialized AI agents that collaborate to understand requests, retrieve business data and policy knowledge, make eligibility decisions, escalate sensitive actions for human approval, and communicate resolutions to customers via real email.

## Architecture

Customer Request
↓
Sentiment & Ticketing Agent → logs a support ticket (sentiment + priority)
↓
Manager Agent → delegates to specialists (hierarchical mode)
↓
Order Agent RAG/Knowledge Agent
(SQLite lookup) (ChromaDB policy search)
↓ ↓
└────────┬────────────┘
↓
Decision Agent
(eligibility + $50 approval threshold)
↓
[Human Approval Layer] ← if refund ≥ $50
↓
Communication Agent
(writes + sends email via SMTP)


## Agents

| Agent | Role |
|---|---|
| Manager Agent | Delegates tasks dynamically (hierarchical mode) |
| Order Agent | Looks up order/customer details from the SQLite database |
| RAG/Knowledge Agent | Searches company policies (delivery, refund, warranty) via ChromaDB |
| Decision Agent | Determines refund/replacement eligibility and approval requirements |
| Communication Agent | Writes and sends professional customer emails via SMTP |
| Sentiment & Ticketing Agent | Analyzes tone/urgency and auto-creates support tickets |

## Tech Stack

- **Language:** Python 3.12
- **Agent Framework:** CrewAI
- **LLM:** Google Gemini (gemini-3.5-flash-lite)
- **RAG:** LangChain + ChromaDB + Gemini Embeddings
- **Database:** SQLite (customers, orders, approvals, tickets)
- **Frontend:** Streamlit
- **Email:** SMTP (Gmail)

## Project Structure

## Project Structure

```
aura-project/
├── app/
│   ├── config/
│   │   └── settings.py          # centralized env vars, model config, business rules
│   ├── database/
│   │   ├── models.py             # schema + seed data
│   │   └── db.py                 # connection helper
│   ├── knowledge_base/
│   │   ├── ingestion.py          # RAG document chunking + embedding
│   │   └── vectorstore.py        # Chroma query interface
│   ├── tools/
│   │   ├── order_tools.py
│   │   ├── policy_tools.py
│   │   ├── approval_tools.py
│   │   ├── ticket_tools.py
│   │   └── email_tools.py
│   ├── agents/
│   │   ├── definitions.py        # the 6 Agent objects
│   │   └── tasks.py               # Task builders
│   └── services/
│       ├── crew_service.py       # build_crew() / build_hierarchical_crew()
│       └── email_service.py      # SMTP sending logic
├── database/
│   └── aura.db                    # SQLite database (generated)
├── knowledge_base/
│   ├── delivery_policy.txt
│   ├── refund_policy.txt
│   ├── warranty_policy.txt
│   └── chroma_store/               # vector store (generated)
├── dashboard/
│   └── main.py                     # Streamlit dashboard (5 pages)
├── .env
└── requirements.txt
```


## Setup

1. Create a virtual environment and install dependencies:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


2. Add your credentials to `.env`:
GOOGLE_API_KEY=your_gemini_api_key
SMTP_EMAIL=your_gmail_address
SMTP_APP_PASSWORD=your_gmail_app_password


3. Build the database and knowledge base:
python database/setup_db.py
python knowledge_base/build_vectorstore.py


4. Launch the dashboard:
streamlit run dashboard/app.py



## Key Features Demonstrated

- Multi-agent collaboration with both sequential and hierarchical (dynamic Manager delegation) processes
- RAG-based knowledge retrieval over company policy documents
- Human-in-the-loop approval workflow for refunds ≥ $50
- Real email automation via SMTP
- Sentiment analysis and automatic support ticket creation
- Live monitoring dashboard for orders, agent runs, approvals, and tickets

## Example Scenario

> "My order ORD1052 has not arrived. Can I get a refund?"

The system: looks up the order, checks delivery delay against today's date, retrieves the applicable refund policy, determines eligibility, escalates for approval if the amount is ≥ $50, and sends the customer a personalized resolution email.

## Notes

- n8n was evaluated as an automation layer but deemed unnecessary, since CrewAI's task/tool architecture already handles the workflow orchestration and automation described in the original proposal.
- Free-tier Gemini API quota (20 req/day on gemini-3.6-flash) required switching to gemini-3.5-flash-lite for reliable testing.