# AURA System Architecture

## Overview

AURA (Autonomous Unified Response & Operations) is a multi-agent AI system that automates customer support operations for a business's order, refund, and warranty inquiries. It combines LLM-based agents, a RAG knowledge base, a relational business database, and human-in-the-loop approval into a single automated pipeline.

## High-Level Flow

Customer Request (text)
|
v
Sentiment & Ticketing Agent --> logs a support ticket (sentiment + priority)
|
v
[Sequential Mode] [Hierarchical Mode]
Fixed pipeline order OR Manager Agent dynamically
delegates to specialists
| |
v v
Order Agent <----> RAG/Knowledge Agent (run in parallel/either order)
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



## Layers

### 1. Configuration (`app/config/`)
Centralizes all environment variables, model settings, and business rules (e.g. the $50 approval threshold) in one place (`settings.py`). Supports both local `.env` files and Streamlit Cloud's secrets manager, with automatic fallback to a writable temp directory for the database/vector store when the deployed filesystem is read-only.

### 2. Database (`app/database/`)
A normalized SQLite schema with four tables: `customers`, `orders`, `approvals`, and `tickets`. `orders.customer_id` is a foreign key into `customers`, allowing proper joins instead of duplicating customer data on every order row.

### 3. Knowledge Base / RAG (`app/knowledge_base/`)
A modular retrieval-augmented generation pipeline:
- `loader.py` — reads both `.txt` and `.pdf` source documents
- `cleaner.py` — normalizes raw text (strips BOM characters, collapses whitespace) before chunking
- `chunker.py` — splits cleaned documents into overlapping chunks
- `embeddings.py` — provides a swappable embedding backend (local `sentence-transformers` for development, Gemini embeddings for production) via a config flag
- `reranker.py` — a hybrid dense+sparse reranker that re-scores vector-retrieved candidates using lexical keyword overlap, improving precision over naive top-k similarity search
- `ingestion.py` / `vectorstore.py` — orchestrate the full build and query pipeline

### 4. Tools (`app/tools/`)
CrewAI tool wrappers exposed to agents: order lookup, policy search, approval-request creation, ticket creation, and email sending. Each tool is logged via the shared logger.

### 5. Agents (`app/agents/`)
Six agents, each in its own file: `sentiment_agent`, `order_agent`, `rag_agent`, `decision_agent`, `communication_agent`, and `manager_agent`. A shared `llm_config.py` provides the single Gemini LLM instance all agents use. Task builders live in `app/agents/tasks/`, one file per task, mirroring the agent structure.

### 6. Services (`app/services/`)
- `crew_service.py` — assembles agents and tasks into a runnable CrewAI `Crew`, supporting both sequential and hierarchical processes
- `email_service.py` — the underlying SMTP sending logic used by the email tool

### 7. Interfaces
- `dashboard/main.py` — a password-protected Streamlit dashboard with five pages: Overview, Orders, Run Agent, Approvals, and Tickets
- `api/routes.py` — a FastAPI REST layer exposing `/run-agent`, `/orders/{id}`, `/tickets`, and `/approvals/pending`, allowing AURA to be called from outside the dashboard

### 8. Tests (`tests/`)
Pytest unit tests covering tool logic, database integrity (including referential integrity between orders and customers), and RAG pipeline components (text cleaning, reranker scoring) — all runnable without invoking the LLM.

## Key Design Decisions

- **Modular RAG over a monolithic pipeline**: separating load/clean/chunk/embed/rerank into distinct files makes each stage independently testable and swappable (e.g. changing embedding providers without touching chunking logic).
- **Policy-grounded decision making**: the Decision Agent is explicitly instructed never to invent exceptions or approve requests that don't meet documented policy criteria, and never to create approval requests for orders that don't exist in the database.
- **Local embeddings for development**: avoids Gemini API rate limits during iterative testing; swappable to Gemini embeddings for production via a single config flag.
- **n8n was evaluated and deliberately excluded**: CrewAI's task/tool architecture already provides the workflow orchestration the original proposal described for n8n, so adding it would have duplicated functionality without adding capability.