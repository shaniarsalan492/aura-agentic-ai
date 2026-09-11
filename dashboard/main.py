import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import sqlite3
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_password():
    """Simple password gate using Streamlit session state and secrets."""
    def password_entered():
        try:
            correct_password = st.secrets.get("DASHBOARD_PASSWORD")
        except Exception:
            correct_password = None
        if correct_password is None:
            correct_password = os.getenv("DASHBOARD_PASSWORD", "aura2026")

        if st.session_state.get("password_input") == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.text_input("Enter password to access AURA Dashboard", type="password",
                   on_change=password_entered, key="password_input")
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("Incorrect password.")
    return False


if not check_password():
    st.stop()


from app.database.models import create_database, seed_sample_data
from app.knowledge_base.ingestion import build_vectorstore

if not os.path.exists("database/aura.db"):
    create_database()
    seed_sample_data()

if not os.path.exists("knowledge_base/chroma_store"):
    build_vectorstore()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "aura.db")

st.set_page_config(page_title="AURA Dashboard", layout="wide")

st.title("🤖 AURA — Autonomous Unified Response & Operations")
st.caption("Multi-Agent Business Operations Dashboard")

page = st.sidebar.radio("Navigate", ["Overview", "Orders", "Run Agent", "Approvals", "Tickets"])


def get_connection():
    return sqlite3.connect(DB_PATH)


# --- OVERVIEW PAGE ---
if page == "Overview":
    st.header("System Overview")

    conn = get_connection()
    cursor = conn.cursor()

    total_orders = cursor.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    delayed_orders = cursor.execute(
        "SELECT COUNT(*) FROM orders WHERE delivery_status = 'Delayed'"
    ).fetchone()[0]
    pending_approvals = cursor.execute(
        "SELECT COUNT(*) FROM approvals WHERE status = 'pending'"
    ).fetchone()[0]

    conn.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", total_orders)
    col2.metric("Delayed Orders", delayed_orders)
    col3.metric("Pending Approvals", pending_approvals)

    st.divider()
    st.subheader("Agent Pipeline")
    st.markdown("""
    **Manager Agent** → routes requests to:
    - 📦 Order Agent
    - 📚 RAG/Knowledge Agent
    - ⚖️ Decision Agent
    - ✉️ Communication Agent
    - 👤 Human Approval Layer (for refunds $50+)
    """)

# --- ORDERS PAGE ---
elif page == "Orders":
    st.header("Order Database")

    conn = get_connection()
    orders = conn.execute("""
        SELECT o.order_id, c.customer_name, o.product_name, o.quantity,
               o.price, o.order_status, o.delivery_status, o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
    """).fetchall()
    conn.close()

    columns = ["Order ID", "Customer", "Product", "Qty", "Price", "Order Status", "Delivery Status", "Date"]
    df = pd.DataFrame(orders, columns=columns)
    st.dataframe(df, width="stretch")

# --- RUN AGENT PAGE ---
elif page == "Run Agent":
    st.header("Run AURA on a Customer Request")
    request_text = st.text_area(
        "Customer Request",
        placeholder="e.g. My order ORD1052 has not arrived. Can I get a refund?"
    )

    mode = st.radio("Pipeline Mode", ["Sequential (faster, fewer API calls)", "Hierarchical (true Manager delegation)"])

    st.caption("⚠️ Please wait for the pipeline to finish before switching pages — navigating away mid-run will cancel it.")

    if st.button("Run AURA Pipeline"):
        if not request_text.strip():
            st.error("Please enter a customer request.")
        else:
            with st.spinner("AURA agents are working on this..."):
                from app.services.crew_service import build_crew, build_hierarchical_crew

                try:
                    if mode.startswith("Sequential"):
                        crew = build_crew(request_text)
                    else:
                        crew = build_hierarchical_crew(request_text)

                    result = crew.kickoff()
                    st.session_state["last_result"] = str(result)
                    st.session_state["last_error"] = None
                except Exception as e:
                    st.session_state["last_result"] = None
                    st.session_state["last_error"] = str(e)

    if st.session_state.get("last_error"):
        st.error(f"Something went wrong: {st.session_state['last_error']}")
    elif st.session_state.get("last_result"):
        st.success("Done!")
        st.subheader("Final Output")
        st.markdown(st.session_state["last_result"])

# --- APPROVALS PAGE ---
elif page == "Approvals":
    st.header("Pending Human Approvals")

    conn = get_connection()
    approvals = conn.execute(
        "SELECT approval_id, order_id, request_type, status, created_at FROM approvals WHERE status = 'pending'"
    ).fetchall()

    if not approvals:
        st.info("No pending approvals.")
    else:
        for approval_id, order_id, request_type, status, created_at in approvals:
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                col1.write(f"**Order:** {order_id} — **Type:** {request_type}  \n*Requested: {created_at}*")
                if col2.button("✅ Approve", key=f"approve_{approval_id}"):
                    conn.execute("UPDATE approvals SET status = 'approved' WHERE approval_id = ?", (approval_id,))
                    conn.commit()
                    st.rerun()
                if col3.button("❌ Reject", key=f"reject_{approval_id}"):
                    conn.execute("UPDATE approvals SET status = 'rejected' WHERE approval_id = ?", (approval_id,))
                    conn.commit()
                    st.rerun()

    conn.close()

# --- TICKETS PAGE ---
elif page == "Tickets":
    st.header("Support Tickets")

    conn = get_connection()
    tickets = conn.execute(
        "SELECT ticket_id, order_id, sentiment, priority, summary, status, created_at FROM tickets ORDER BY ticket_id DESC"
    ).fetchall()
    conn.close()

    if not tickets:
        st.info("No tickets yet.")
    else:
        columns = ["Ticket ID", "Order ID", "Sentiment", "Priority", "Summary", "Status", "Created"]
        df = pd.DataFrame(tickets, columns=columns)
        st.dataframe(df, width="stretch")