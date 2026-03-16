from fastapi import APIRouter, HTTPException

from src.schemas.email import EmailRequest, EmailResponse
from src.services.email_parser import parse_email
from src.services.followup_tracker import get_pending_followups, get_followup
from src.services.email_store import create_email_record, update_email_record
from src.graph.workflow import email_agent_graph
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/email/process", response_model=EmailResponse)
async def process_email(request: EmailRequest):
    """Process an incoming customer support email through the agent graph."""
    logger.info("Received email from %s: %s", request.from_email, request.subject)

    # Create email record in store
    email_record = create_email_record(
        from_email=request.from_email,
        subject=request.subject,
        body=request.body,
    )

    # Parse and normalize
    parsed = parse_email(request.model_dump())

    # Build initial state
    initial_state = {
        "email_from": parsed["email_from"],
        "email_subject": parsed["email_subject"],
        "email_body": parsed["email_body"],
        "category": None,
        "sentiment": None,
        "kb_context": None,
        "draft_response": None,
        "final_response": None,
        "quality_approved": None,
        "revision_count": 0,
        "requires_followup": None,
        "followup_reason": None,
        "conversation_id": request.conversation_id,
        "status": "received",
        "messages": [],
    }

    # Run the graph
    result = await email_agent_graph.ainvoke(initial_state)

    # Update email record with results
    update_email_record(
        email_record["email_id"],
        category=result.get("category", "other"),
        sentiment=result.get("sentiment", "neutral"),
        reply_body=result.get("final_response", ""),
        status=result.get("status", "error"),
        conversation_id=result.get("conversation_id"),
        requires_followup=result.get("requires_followup", False),
    )

    return EmailResponse(
        reply_body=result.get("final_response", ""),
        category=result.get("category", "other"),
        sentiment=result.get("sentiment", "neutral"),
        status=result.get("status", "error"),
        requires_followup=result.get("requires_followup", False),
        followup_reason=result.get("followup_reason"),
        conversation_id=result.get("conversation_id"),
    )


@router.get("/followups")
async def list_followups():
    """List all pending follow-ups."""
    return {"followups": get_pending_followups()}


@router.get("/followups/{conversation_id}")
async def get_followup_detail(conversation_id: str):
    """Get follow-up details for a specific conversation."""
    followup = get_followup(conversation_id)
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return followup
