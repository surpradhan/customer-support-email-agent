"""Parse and normalize incoming email data."""

import re


def parse_email(raw_email: dict) -> dict:
    """Extract and clean fields from a raw email payload."""
    body = raw_email.get("body", "")

    # Strip excessive whitespace and normalize line breaks
    body = re.sub(r"\r\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = body.strip()

    return {
        "email_from": raw_email.get("from_email", "").strip(),
        "email_subject": raw_email.get("subject", "").strip(),
        "email_body": body,
    }
