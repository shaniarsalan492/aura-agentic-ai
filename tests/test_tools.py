"""Unit tests for AURA's tools. These test the underlying logic directly
(bypassing the LLM/agent layer) using pytest's .func attribute to call
the raw Python function wrapped by CrewAI's @tool decorator."""

import pytest
from app.tools.order_tools import order_lookup_tool
from app.tools.policy_tools import policy_search_tool
from app.tools.approval_tools import create_approval_request
from app.tools.ticket_tools import create_ticket_tool


def test_order_lookup_finds_existing_order():
    result = order_lookup_tool.func(order_id="ORD1052")
    assert "Ali Khan" in result
    assert "ORD1052" in result


def test_order_lookup_handles_missing_order():
    result = order_lookup_tool.func(order_id="ORD9999")
    assert "No order found" in result


def test_policy_search_returns_relevant_content():
    result = policy_search_tool.func(query="refund policy for delayed orders")
    assert "refund" in result.lower() or "delay" in result.lower()
    assert len(result) > 0


def test_approval_request_creates_pending_entry():
    result = create_approval_request.func(order_id="ORD1052", request_type="refund")
    assert "Approval request created" in result
    assert "ORD1052" in result


def test_ticket_creation_returns_confirmation():
    result = create_ticket_tool.func(
        order_id="ORD1052",
        customer_id="CUST001",
        sentiment="neutral",
        priority="low",
        summary="Test ticket for automated testing."
    )
    assert "Ticket created" in result
    assert "ORD1052" in result