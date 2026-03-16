"""LangGraph workflow definition for the customer support email agent."""

from langgraph.graph import StateGraph, START, END

from src.schemas.state import EmailAgentState
from src.graph.nodes import (
    classify_email,
    research,
    draft_response,
    quality_check,
    send_response,
)


def should_redraft(state: EmailAgentState) -> str:
    """Route after quality check: redraft if not approved, otherwise send."""
    if state.get("quality_approved"):
        return "send"
    return "draft"


def build_graph() -> StateGraph:
    """Construct and compile the email agent graph."""
    graph = StateGraph(EmailAgentState)

    # Add nodes — names must not collide with state keys
    graph.add_node("classify", classify_email)
    graph.add_node("research", research)
    graph.add_node("draft", draft_response)
    graph.add_node("review", quality_check)
    graph.add_node("send", send_response)

    # Define edges
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "research")
    graph.add_edge("research", "draft")
    graph.add_edge("draft", "review")

    # Conditional: quality check can loop back to draft or proceed to send
    graph.add_conditional_edges(
        "review",
        should_redraft,
        {
            "draft": "draft",
            "send": "send",
        },
    )

    graph.add_edge("send", END)

    return graph.compile()


# Compiled graph singleton
email_agent_graph = build_graph()
