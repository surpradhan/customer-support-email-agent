from src.services.email_parser import parse_email
from src.services.knowledge_base import search_kb
from src.services.followup_tracker import (
    create_conversation_id,
    record_followup,
    get_followup,
    resolve_followup,
    get_pending_followups,
)


class TestEmailParser:
    def test_parse_basic_email(self):
        raw = {
            "from_email": " user@example.com ",
            "subject": " Help needed ",
            "body": "I need help\r\nwith my account",
        }
        result = parse_email(raw)
        assert result["email_from"] == "user@example.com"
        assert result["email_subject"] == "Help needed"
        assert "\r\n" not in result["email_body"]

    def test_parse_strips_excessive_newlines(self):
        raw = {
            "from_email": "a@b.com",
            "subject": "test",
            "body": "line1\n\n\n\n\nline2",
        }
        result = parse_email(raw)
        assert result["email_body"] == "line1\n\nline2"


class TestKnowledgeBase:
    def test_search_returns_results_for_refund(self):
        result = search_kb("refund policy money back guarantee")
        assert "refund" in result.lower()

    def test_search_returns_results_for_password(self):
        result = search_kb("how to reset my password")
        assert "password" in result.lower()

    def test_search_returns_content(self):
        result = search_kb("billing subscription payment")
        assert len(result) > 0
        assert "No relevant articles" not in result


class TestFollowupTracker:
    def test_create_and_retrieve_followup(self):
        cid = create_conversation_id()
        record_followup(cid, "a@b.com", "complaint", "Needs manager review", "Billing issue")
        followup = get_followup(cid)
        assert followup is not None
        assert followup["email_from"] == "a@b.com"
        assert followup["resolved"] is False

    def test_resolve_followup(self):
        cid = create_conversation_id()
        record_followup(cid, "a@b.com", "complaint", "test", "test")
        assert resolve_followup(cid) is True
        assert get_followup(cid)["resolved"] is True

    def test_resolve_nonexistent(self):
        assert resolve_followup("nonexistent") is False

    def test_pending_followups(self):
        cid = create_conversation_id()
        record_followup(cid, "x@y.com", "inquiry", "waiting", "Question")
        pending = get_pending_followups()
        assert any(f["conversation_id"] == cid for f in pending)
