"""Inbox management and history endpoints."""

from fastapi import APIRouter, HTTPException, Query
from src.services.email_store import get_email, list_emails, get_stats
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/inbox/stats")
async def get_inbox_stats():
    """Get inbox statistics."""
    return get_stats()


@router.get("/inbox")
async def list_inbox_emails(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List all emails in the inbox (paginated)."""
    emails, total = list_emails(limit=limit, offset=offset)
    return {
        "emails": emails,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/inbox/{email_id}")
async def get_inbox_email(email_id: str):
    """Get details of a specific email."""
    email = get_email(email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email
