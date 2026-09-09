from crewai import Crew, Process
from app.agents.definitions import (
    sentiment_agent, order_agent, rag_agent, decision_agent, communication_agent, manager_agent
)
from app.agents.tasks import (
    build_sentiment_task, build_order_task, build_policy_task,
    build_decision_task, build_communication_task, build_main_task
)


def build_crew(customer_request: str) -> Crew:
    sentiment_task = build_sentiment_task(customer_request)
    order_task = build_order_task(customer_request)
    policy_task = build_policy_task(customer_request)
    decision_task = build_decision_task(customer_request, order_task, policy_task)
    communication_task = build_communication_task(order_task, decision_task)

    return Crew(
        agents=[sentiment_agent, order_agent, rag_agent, decision_agent, communication_agent],
        tasks=[sentiment_task, order_task, policy_task, decision_task, communication_task],
        process=Process.sequential,
        verbose=True
    )


def build_hierarchical_crew(customer_request: str) -> Crew:
    main_task = build_main_task(customer_request)

    return Crew(
        agents=[order_agent, rag_agent, decision_agent, communication_agent],
        tasks=[main_task],
        process=Process.hierarchical,
        manager_agent=manager_agent,
        verbose=True
    )


if __name__ == "__main__":
    request = "My order ORD1052 has not arrived. Can I get a refund?"
    crew = build_crew(request)
    result = crew.kickoff()
    print("\n\n=== FINAL RESULT ===\n")
    print(result)