# Week 2 — Conversational API

## Scripts

### script10_chat.py

Extends script9 from a single-question endpoint to a full conversational API.
The server is stateless — it holds no session data. The client sends the full
message history on every request, and the server passes it to Claude as context.
This is the same pattern Anthropic and OpenAI use in their own APIs.

**Key question:** How do you constrain a field to specific string values in Pydantic?
**Answer:** Use `Literal["user", "assistant"]` from the `typing` module as the type
annotation. No `Field()` needed — the type alone does the validation. `Enum` would
work too but adds unnecessary complexity for a simple two-value constraint.

**Key question:** How do you declare a list of validated objects in Pydantic?
**Answer:** `messages: list[MessageBody]` — Pydantic validates every item in the
list against the `MessageBody` model automatically.

**Key question:** What are the valid values Claude returns for `stop_reason`?
**Answer:** `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn`, `refusal`.
Typed as `Literal` in the response model so any unexpected value raises a validation error.

**Key question:** What does stateless memory mean in this API?
**Answer:** The server stores nothing between requests. The client owns the conversation
history and sends the full `messages` array every time. The server reads it, passes it
to Claude, and returns the response. State lives in the client, not the server.

-----

## How to run

```bash
uvicorn script10_chat:app --reload
```

## Test with

Single turn:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is a large language model?"}]}'
```

Multi-turn (tests memory):

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "My name is Aravindhan."},
      {"role": "assistant", "content": "Nice to meet you Aravindhan!"},
      {"role": "user", "content": "What is my name?"}
    ]
  }'
```

Validation failure (expects 422):

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "banana", "content": "hello"}]}'
```