"""Graph node functions — each receives the agent state and returns updates."""

import json
from langchain_core.messages import HumanMessage

from src.core.llm import get_llm
from src.prompts.templates import (
    CLASSIFICATION_PROMPT,
    DRAFT_RESPONSE_PROMPT,
    QUALITY_CHECK_PROMPT,
    RESEARCH_QUERY_PROMPT,
)
from src.services.knowledge_base import search_kb
from src.services.followup_tracker import record_followup, create_conversation_id
from src.schemas.state import EmailAgentState
from src.utils.logger import get_logger

logger = get_logger(__name__)
MAX_REVISIONS = 2


async def classify_email(state: EmailAgentState) -> dict:
    """Classify the email into a support category and detect sentiment."""
    logger.info("Classifying email: %s", state["email_subject"])
    llm = get_llm()

    prompt = CLASSIFICATION_PROMPT.format(
        subject=state["email_subject"],
        body=state["email_body"],
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])

    try:
        result = json.loads(response.content)
        category = result.get("category", "other")
        sentiment = result.get("sentiment", "neutral")
    except (json.JSONDecodeError, AttributeError):
        logger.warning("Failed to parse classification JSON, falling back to defaults. Raw response: %s", response.content)
        category = "other"
        sentiment = "neutral"

    logger.info("Classified as category=%s, sentiment=%s", category, sentiment)
    return {
        "category": category,
        "sentiment": sentiment,
        "status": "classified",
        "messages": [HumanMessage(content=prompt), response],
    }


async def research(state: EmailAgentState) -> dict:
    """Search the knowledge base for relevant context."""
    logger.info("Researching knowledge base for category=%s", state.get("category"))
    llm = get_llm()

    # Use LLM to generate a focused search query
    prompt = RESEARCH_QUERY_PROMPT.format(
        category=state.get("category", ""),
        subject=state["email_subject"],
        body=state["email_body"],
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    search_query = response.content.strip()

    # Search knowledge base
    kb_context = search_kb(query=search_query)
    logger.info("Found KB context (%d chars)", len(kb_context))

    return {
        "kb_context": kb_context,
        "status": "researched",
    }


async def draft_response(state: EmailAgentState) -> dict:
    """Generate a draft reply to the customer."""
    logger.info("Drafting response (revision %d)", state.get("revision_count", 0))
    llm = get_llm()

    prompt = DRAFT_RESPONSE_PROMPT.format(
        category=state.get("category", ""),
        sentiment=state.get("sentiment", ""),
        subject=state["email_subject"],
        body=state["email_body"],
        kb_context=state.get("kb_context", "No context available."),
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])

    return {
        "draft_response": response.content,
        "status": "drafted",
    }


async def quality_check(state: EmailAgentState) -> dict:
    """Review the draft for tone, accuracy, and completeness."""
    logger.info("Running quality check")
    llm = get_llm()

    prompt = QUALITY_CHECK_PROMPT.format(
        body=state["email_body"],
        category=state.get("category", ""),
        kb_context=state.get("kb_context", ""),
        draft=state.get("draft_response", ""),
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])

    try:
        result = json.loads(response.content)
        approved = result.get("approved", False)
        requires_followup = result.get("requires_followup", False)
        followup_reason = result.get("followup_reason", "")
    except (json.JSONDecodeError, AttributeError):
        logger.warning("Failed to parse quality check JSON, falling back to approved=True. Raw response: %s", response.content)
        approved = True
        requires_followup = False
        followup_reason = ""

    revision_count = state.get("revision_count", 0) + 1

    # Force approval if max revisions reached
    if not approved and revision_count >= MAX_REVISIONS:
        logger.warning("Max revisions reached, forcing approval")
        approved = True

    logger.info("Quality check: approved=%s, followup=%s", approved, requires_followup)
    return {
        "quality_approved": approved,
        "requires_followup": requires_followup,
        "followup_reason": followup_reason if requires_followup else None,
        "revision_count": revision_count,
        "status": "reviewed",
    }


async def send_response(state: EmailAgentState) -> dict:
    """Finalize and send the response. Record follow-up if needed."""
    logger.info("Sending final response to %s", state["email_from"])

    conversation_id = state.get("conversation_id") or create_conversation_id()

    # Record follow-up if needed
    if state.get("requires_followup"):
        record_followup(
            conversation_id=conversation_id,
            email_from=state["email_from"],
            category=state.get("category", "other"),
            reason=state.get("followup_reason", ""),
            original_subject=state["email_subject"],
        )

    # In production, this is where you'd call an email sending service
    logger.info("Response sent. conversation_id=%s", conversation_id)

    return {
        "final_response": state.get("draft_response", ""),
        "conversation_id": conversation_id,
        "status": "sent",
    }
