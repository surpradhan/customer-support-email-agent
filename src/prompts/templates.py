"""Prompt templates for each graph node."""

CLASSIFICATION_PROMPT = """\
You are a customer support email classifier. Analyze the email below and respond with ONLY valid JSON.

Categories: complaint, inquiry, refund_request, feedback, technical_issue, other
Sentiments: positive, neutral, negative, urgent

Email subject: {subject}
Email body: {body}

Respond in this exact JSON format:
{{"category": "<category>", "sentiment": "<sentiment>"}}"""

RESEARCH_QUERY_PROMPT = """\
Given this customer email, generate a short search query to find relevant help articles.

Category: {category}
Subject: {subject}
Body: {body}

Respond with only the search query, nothing else."""

DRAFT_RESPONSE_PROMPT = """\
You are a professional and empathetic customer support agent. Draft a reply to the customer email below.

Guidelines:
- Be warm, professional, and empathetic
- Address the customer's specific concern
- Use the knowledge base context to provide accurate information
- If the issue cannot be fully resolved via email, explain the next steps
- Keep the response concise but thorough

Category: {category}
Sentiment: {sentiment}
Customer email subject: {subject}
Customer email body: {body}

Relevant knowledge base information:
{kb_context}

Draft your response (email body only, no subject line):"""

QUALITY_CHECK_PROMPT = """\
Review this customer support email draft. Check for:
1. Professional and empathetic tone
2. Factual accuracy (based on the knowledge base context provided)
3. Completeness — does it address all customer concerns?
4. Appropriate next steps if the issue needs follow-up

Original customer email: {body}
Category: {category}
Knowledge base context: {kb_context}
Draft response: {draft}

Respond in this exact JSON format:
{{"approved": true/false, "feedback": "<specific feedback if not approved, empty string if approved>", "requires_followup": true/false, "followup_reason": "<reason if follow-up needed, empty string otherwise>"}}"""
