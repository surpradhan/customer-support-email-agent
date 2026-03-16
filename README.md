# Customer Support Email Agent

A LangGraph-based agent that processes and responds to customer support emails using LLM-powered classification, routing, and response generation.

## Architecture

The agent uses a LangGraph state machine with the following flow:

1. **Intake** — Parse and normalize incoming email
2. **Classify** — Categorize the email (complaint, inquiry, refund, feedback, etc.)
3. **Research** — Look up relevant knowledge base articles and customer context
4. **Draft** — Generate a response using category-specific prompts
5. **Quality Check** — Validate tone, accuracy, and completeness
6. **Send** — Deliver the final response

## Project Structure

```
src/
├── api/          — FastAPI routes and request handling
├── graph/        — LangGraph workflow definition and nodes
├── services/     — Business logic (email parsing, knowledge base lookup)
├── prompts/      — Prompt templates for each stage
├── schemas/      — Pydantic models for emails, state, and API contracts
├── core/         — App config, settings, and shared dependencies
├── utils/        — Logging, helpers
├── knowledge_base/ — Static support docs and FAQ data
tests/            — Unit and integration tests
```

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then fill in your API keys
```

## Run

```bash
uvicorn src.main:app --reload
```

## Test

```bash
pytest tests/ -v
```
