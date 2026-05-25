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


---

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

---

### script11_streaming.py
Extends script10 by replacing the single-response endpoint with a streaming
response. Instead of waiting for Claude to finish generating, the server
forwards each chunk to the client as it arrives — the same pattern used by
Claude.ai and ChatGPT to render responses word by word.

**Key question:** What is a generator and how does `yield` differ from `return`?
**Answer:** `return` exits the function and sends one value back. `yield` pauses
the function, sends one value back, then resumes from that line on the next
iteration. A function containing `yield` is a generator. FastAPI iterates the
generator chunk by chunk and sends each piece to the client immediately.

**Key question:** Why does `client.messages.stream()` need a `with` block?
**Answer:** Streaming opens a persistent network connection. `with` guarantees
the connection closes even if an exception is thrown mid-stream. Without it,
a crash mid-generator leaks the connection.

**Key question:** Why does this endpoint have no `response_model`?
**Answer:** `response_model` tells FastAPI to validate a complete response object
against a Pydantic model before sending it. Streaming has no complete object —
chunks arrive and are forwarded incrementally. There is nothing to validate upfront.

---

## How to run

```bash
uvicorn script11_streaming:app --reload
```

## Test with

Single turn:

```bash
curl -X POST http://localhost:8000/ask-stream \
  -H "Content-Type: application/json" \
  -d '{"question": "Count from 1 to 10 slowly"}' \
  --no-buffer
```