# AURA — Autonomous Unified Response & Operations

A multi-agent AI business operations system that automates customer support — order inquiries, refunds, and warranty questions — using specialized AI agents, retrieval-augmented generation, a business database, human-in-the-loop approval, and real email automation.

**Live demo:** [add your Streamlit Cloud URL here] (password-protected — see report for access)

## Overview

AURA was built as an individual submission for an Agentic AI course, adapting the original proposal's 3-student team scope into a solo build. It goes beyond a single-purpose chatbot: six specialized agents collaborate, reason over real business data and a 17-page company policy handbook, escalate sensitive decisions to a human, and take real-world action by sending live emails.

## Architecture

Customer Request
|
v
Sentiment & Ticketing Agent --> logs a support ticket (sentiment + priority)
|
v
Sequential Mode Hierarchical Mode
(fixed pipeline order) OR (Manager Agent dynamically
delegates to specialists)
| |
v v
Order Agent <----> RAG/Knowledge Agent
| |
+--------------------+
|
v
Decision Agent
(eligibility + $50 human-approval threshold)
|
[Human Approval Layer] <-- if refund >= $50
|
v
Communication Agent
(writes + sends customer email via SMTP)



Full architectural detail: [`docs/architecture.md`](docs/architecture.md)

## Agents

| Agent | Responsibility |
|---|---|
| Manager Agent | Dynamically delegates work to specialists (hierarchical mode) |
| Order Agent | Looks up order/customer details from the SQLite database |
| RAG/Knowledge Agent | Searches company policy documents via ChromaDB with hybrid reranking |
| Decision Agent | Determines eligibility and whether human approval is required |
| Communication Agent | Writes and sends the customer-facing email via SMTP |
| Sentiment & Ticketing Agent | Classifies tone/urgency and logs a support ticket |

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.12 |
| Agent Framework | CrewAI |
| LLM | Google Gemini (gemini-3.6-flash) |
| RAG | LangChain + ChromaDB, modular load/clean/chunk pipeline, hybrid dense-sparse reranking |
| Embeddings | Local (sentence-transformers/all-MiniLM-L6-v2), swappable to Gemini via config |
| Database | SQLite (customers, orders, approvals, tickets) |
| Frontend | Streamlit (password-protected) |
| API | FastAPI |
| Email | SMTP (Gmail) |
| Testing | pytest |
| Data Validation | Pydantic |

## Project Structure

aura-project/
├── app/
│ ├── config/
│ │ └── settings.py # centralized env vars, model config, business rules
│ ├── database/
│ │ ├── models.py # schema + seed data (100 orders, 50 customers)
│ │ └── db.py # connection helper (writable-dir fallback for cloud)
│ ├── knowledge_base/
│ │ ├── loader.py # loads .txt and .pdf source documents
│ │ ├── cleaner.py # normalizes raw text before chunking
│ │ ├── chunker.py # splits documents into overlapping chunks
│ │ ├── embeddings.py # swappable local/Gemini embedding provider
│ │ ├── reranker.py # hybrid dense+sparse reranking
│ │ ├── ingestion.py # full pipeline: load -> clean -> chunk -> embed -> persist
│ │ └── vectorstore.py # two-stage retrieval: vector search + rerank
│ ├── tools/
│ │ ├── order_tools.py
│ │ ├── policy_tools.py
│ │ ├── approval_tools.py
│ │ ├── ticket_tools.py
│ │ └── email_tools.py
│ ├── agents/
│ │ ├── llm_config.py # shared Gemini LLM instance
│ │ ├── sentiment_agent.py
│ │ ├── order_agent.py
│ │ ├── rag_agent.py
│ │ ├── decision_agent.py
│ │ ├── communication_agent.py
│ │ ├── manager_agent.py
│ │ └── tasks/ # one task builder per agent
│ ├── services/
│ │ ├── crew_service.py # build_crew() / build_hierarchical_crew()
│ │ └── email_service.py # SMTP sending logic
│ ├── models/
│ │ └── schemas.py # Pydantic data models (Order, Ticket, Approval, etc.)
│ └── utils/
│ └── logger.py # structured logging to console + rotating log file
├── api/
│ └── routes.py # FastAPI REST layer
├── dashboard/
│ └── main.py # Streamlit dashboard (password-protected, 5 pages)
├── database/
│ └── aura.db # SQLite database (generated)
├── knowledge_base/
│ ├── delivery_policy.txt
│ ├── refund_policy.txt
│ ├── warranty_policy.txt
│ ├── TechMart_Company_Policy_Handbook.pdf # 17-page, 28-section policy document
│ └── chroma_store/ # vector store (generated)
├── tests/
│ ├── test_tools.py
│ ├── test_database.py
│ └── test_knowledge_base.py
├── docs/
│ └── architecture.md
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt



## Setup

1. Clone the repository and create a virtual environment:

git clone https://github.com/shaniarsalan492/aura-agentic-ai.git
cd aura-agentic-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


2. Copy `.env.example` to `.env` and fill in your credentials:

GOOGLE_API_KEY=your_gemini_api_key
SMTP_EMAIL=your_gmail_address
SMTP_APP_PASSWORD=your_gmail_app_password
DASHBOARD_PASSWORD=your_chosen_password



3. Build the database and knowledge base:

python -m app.database.models
python -m app.knowledge_base.ingestion

4. Launch the dashboard:

streamlit run dashboard/main.py

   Or launch the REST API:

uvicorn api.routes:app --reload --port 8000

   Interactive API docs available at `http://localhost:8000/docs`.

## Running Tests

pytest -v


Tests cover tool logic, database referential integrity, and RAG pipeline components (text cleaning, reranker scoring) — all runnable without calling the LLM.

## Key Features

- Multi-agent collaboration with both sequential and hierarchical (dynamic Manager delegation) processes
- RAG pipeline ingesting both `.txt` and `.pdf` sources, including a 17-page, 28-section company policy handbook
- Hybrid dense+sparse reranking for improved retrieval precision over naive top-k vector search
- Swappable embedding provider (local, free, unlimited for development; Gemini for production)
- Human-in-the-loop approval workflow for refunds ≥ $50
- Real email automation via SMTP
- Sentiment analysis and automatic support ticket creation
- REST API layer (FastAPI) alongside the Streamlit dashboard
- Password-protected live deployment
- Automated test suite (pytest)
- Structured logging with rotating log files
- Pydantic-validated data schemas

## Example Scenario

> "My order ORD1052 has not arrived. Can I get a refund?"

The system: logs a support ticket with sentiment/priority, looks up the order, calculates the actual delay against today's date, retrieves the applicable refund policy, determines eligibility, escalates for human approval if the amount is ≥ $50, and sends the customer a personalized resolution email — all traceable through structured logs.

## Design Notes

- **n8n was evaluated and deliberately excluded.** CrewAI's task/tool architecture already provides the workflow orchestration and automation the original proposal described for n8n; adding it would have duplicated existing functionality without adding real capability.
- **Local embeddings as a development strategy.** Free-tier Gemini API quotas (as low as 20 requests/day on newer models) made local embeddings the practical choice for iterative testing, with Gemini embeddings available via a config toggle for production.
- **Policy-grounded decision making.** The Decision Agent is explicitly constrained to never invent "exception" approval paths outside documented policy, and never to create approval requests for orders that don't exist in the database — verified through both manual testing and automated tests.

## Author

Built individually as a solo submission for the Agentic AI course project, adapting the original 3-student proposal scope.