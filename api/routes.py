import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.crew_service import build_crew, build_hierarchical_crew
from app.database.db import get_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="AURA API",
    description="Multi-agent AI business operations system — REST interface",
    version="1.0.0"
)

pipeline_lock = threading.Lock()


class CustomerRequest(BaseModel):
    message: str
    mode: str = "sequential"  # "sequential" or "hierarchical"


class RunResponse(BaseModel):
    success: bool
    result: str


@app.get("/")
def root():
    return {"service": "AURA API", "status": "running"}


@app.post("/run-agent", response_model=RunResponse)
def run_agent(request: CustomerRequest):
    """Runs the AURA multi-agent pipeline on a customer request and returns the result.
    Only one pipeline run is allowed at a time (the underlying local embedding model
    is not safely reusable across concurrent threads); overlapping requests receive
    a 429 response asking the caller to retry shortly."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="message cannot be empty")

    logger.info(f"API request received | mode={request.mode} | message={request.message[:80]}")

    if not pipeline_lock.acquire(blocking=False):
        raise HTTPException(
            status_code=429,
            detail="Another request is currently being processed. Please try again shortly."
        )

    try:
        if request.mode == "hierarchical":
            crew = build_hierarchical_crew(request.message)
        else:
            crew = build_crew(request.message)

        result = crew.kickoff()
        return RunResponse(success=True, result=str(result))

    except Exception as e:
        logger.error(f"API pipeline error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        pipeline_lock.release()


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    """Fetch a single order's details directly from the database (no agent involved)."""
    conn = get_connection()
    row = conn.execute("""
        SELECT o.order_id, c.customer_name, c.email, o.product_name, o.quantity,
               o.price, o.order_status, o.delivery_status, o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_id = ?
    """, (order_id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    columns = ["order_id", "customer_name", "customer_email", "product_name",
               "quantity", "price", "order_status", "delivery_status", "order_date"]
    return dict(zip(columns, row))


@app.get("/tickets")
def get_tickets():
    """Returns all support tickets, most recent first."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT ticket_id, order_id, sentiment, priority, summary, status, created_at "
        "FROM tickets ORDER BY ticket_id DESC"
    ).fetchall()
    conn.close()

    columns = ["ticket_id", "order_id", "sentiment", "priority", "summary", "status", "created_at"]
    return [dict(zip(columns, row)) for row in rows]


@app.get("/approvals/pending")
def get_pending_approvals():
    """Returns all pending human approval requests."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT approval_id, order_id, request_type, status, created_at "
        "FROM approvals WHERE status = 'pending'"
    ).fetchall()
    conn.close()

    columns = ["approval_id", "order_id", "request_type", "status", "created_at"]
    return [dict(zip(columns, row)) for row in rows]