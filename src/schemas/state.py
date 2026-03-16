from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class EmailAgentState(TypedDict):
    """State that flows through the LangGraph nodes."""

    # Incoming email fields
    email_from: str
    email_subject: str
    email_body: str

    # Classification
    category: Optional[str]
    sentiment: Optional[str]

    # Knowledge base
    kb_context: Optional[str]

    # Response generation
    draft_response: Optional[str]
    final_response: Optional[str]
    quality_approved: Optional[bool]
    revision_count: int

    # Follow-up tracking
    requires_followup: Optional[bool]
    followup_reason: Optional[str]
    conversation_id: Optional[str]

    # Processing status
    status: str

    # LLM message history
    messages: Annotated[list[BaseMessage], add_messages]
