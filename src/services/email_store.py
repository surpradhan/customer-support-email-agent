"""In-memory email store for testing and tracking all processed emails."""

import uuid
from datetime import datetime, timezone
from src.utils.logger import get_logger

logger = get_logger(__name__)

# In-memory email store: {email_id: email_record}
_emails: dict[str, dict] = {}


def create_email_record(
    from_email: str,
    subject: str,
    body: str,
) -> dict:
    """Create a new email record before processing."""
    email_id = str(uuid.uuid4())
    record = {
        "email_id": email_id,
        "from_email": from_email,
        "subject": subject,
        "body": body,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "processed_at": None,
        "category": None,
        "sentiment": None,
        "reply_body": None,
        "status": "pending",
        "conversation_id": None,
        "requires_followup": False,
    }
    _emails[email_id] = record
    logger.info("Created email record: %s", email_id)
    return record


def update_email_record(email_id: str, **updates) -> dict | None:
    """Update an email record with processing results."""
    if email_id not in _emails:
        return None
    record = _emails[email_id]
    record.update(updates)
    record["processed_at"] = datetime.now(timezone.utc).isoformat()
    logger.info("Updated email record: %s", email_id)
    return record


def get_email(email_id: str) -> dict | None:
    """Get a single email record."""
    return _emails.get(email_id)


def list_emails(limit: int = 50, offset: int = 0) -> tuple[list[dict], int]:
    """List all emails (paginated), newest first."""
    emails = sorted(_emails.values(), key=lambda x: x["created_at"], reverse=True)
    total = len(emails)
    paginated = emails[offset : offset + limit]
    return paginated, total


def get_stats() -> dict:
    """Get inbox statistics."""
    emails = _emails.values()
    return {
        "total": len(emails),
        "pending": sum(1 for e in emails if e["status"] == "pending"),
        "sent": sum(1 for e in emails if e["status"] == "sent"),
        "requires_followup": sum(1 for e in emails if e.get("requires_followup")),
    }
