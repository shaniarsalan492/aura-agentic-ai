from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CustomerSchema(BaseModel):
    customer_id: str
    customer_name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class OrderSchema(BaseModel):
    order_id: str
    customer_id: str
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    product_name: str
    quantity: int = Field(gt=0)
    price: Optional[float] = Field(default=None, ge=0)
    order_status: str
    delivery_status: str
    order_date: str


class ApprovalSchema(BaseModel):
    approval_id: Optional[int] = None
    order_id: str
    request_type: str
    status: str = "pending"
    created_at: Optional[str] = None


class TicketSchema(BaseModel):
    ticket_id: Optional[int] = None
    order_id: Optional[str] = None
    customer_id: Optional[str] = None
    sentiment: str
    priority: str
    summary: str
    status: str = "open"
    created_at: Optional[str] = None


class AgentResponseSchema(BaseModel):
    """Generic wrapper for structured agent output, useful for API responses."""
    success: bool
    message: str
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)