"""In-memory follow-up tracker for conversations requiring further action."""

import uuid
from datetime import datetime, timezone
from src.utils.logger import get_logger

logger = get_logger(__name__)

# In-memory store — swap with a database in production
_followups: dict[str, dict] = {}


def create_conversation_id() -> str:
    return str(uuid.uuid4())


def record_followup(
    conversation_id: str,
    email_from: str,
    category: str,
    reason: str,
    original_subject: str,
) -> dict:
    """Record that a conversation requires follow-up."""
    entry = {
        "conversation_id": conversation_id,
        "email_from": email_from,
        "category": category,
        "reason": reason,
        "original_subject": original_subject,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "resolved": False,
    }
    _followups[conversation_id] = entry
    logger.info("Follow-up recorded: %s — %s", conversation_id, reason)
    return entry


def get_followup(conversation_id: str) -> dict | None:
    return _followups.get(conversation_id)


def resolve_followup(conversation_id: str) -> bool:
    if conversation_id in _followups:
        _followups[conversation_id]["resolved"] = True
        _followups[conversation_id]["resolved_at"] = datetime.now(timezone.utc).isoformat()
        logger.info("Follow-up resolved: %s", conversation_id)
        return True
    return False


def get_pending_followups() -> list[dict]:
    return [f for f in _followups.values() if not f["resolved"]]
