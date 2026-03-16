from typing import Optional
from pydantic import BaseModel


class EmailRequest(BaseModel):
    from_email: str
    subject: str
    body: str
    conversation_id: Optional[str] = None


class EmailResponse(BaseModel):
    reply_body: str
    category: str
    sentiment: str
    status: str
    requires_followup: bool = False
    followup_reason: Optional[str] = None
    conversation_id: Optional[str] = None
