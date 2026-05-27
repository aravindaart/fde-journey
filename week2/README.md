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
      {"role": "user", "content": "My name is Alex."},
      {"role": "assistant", "content": "Nice to meet you Alex!"},
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

Deployed and tested on Render. Streaming confirmed working on live endpoint.

---


### script12_context.py

Extends script10 with context window management. After Pydantic validation, 
the message list is passed through compact_messages before reaching Claude — 
dropping the oldest messages to keep token usage bounded.

**Key question:** Which end of the messages array do you drop from — the start or the end?
**Answer:** Drop the oldest messages. You always keep the most recent ones because they're most relevant to the current question.

**Key question:** Where should the trimming happen — on the client before sending, or on the server after receiving? 
**Answer:** Server-side is non-negotiable. Client trims to avoid sending unnecessary data, server trims as a safety net because you never trust the client.

**Key question:** What would you do if the conversation history is getting too long — what's the simplest strategy to handle it?
**Answer:** Two strategies exist. Compaction summarises old messages into one — better 
quality but costs an extra Claude call. Sliding window keeps only the last 
N messages and drops the oldest — cheap, fast, no extra API call.

---

## How to run

```bash
uvicorn script12_context:app --reload
```

## Test with

Quick turn:

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

Using compact_message:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Message 1"},
      {"role": "assistant", "content": "Response 1"},
      {"role": "user", "content": "Message 2"},
      {"role": "assistant", "content": "Response 2"},
      {"role": "user", "content": "Message 3"},
      {"role": "assistant", "content": "Response 3"},
      {"role": "user", "content": "Message 4"},
      {"role": "assistant", "content": "Response 4"},
      {"role": "user", "content": "Message 5"},
      {"role": "assistant", "content": "Response 5"},
      {"role": "user", "content": "Message 6"},
      {"role": "assistant", "content": "Response 6"},
      {"role": "user", "content": "What was message 1?"}
    ]
  }'
```

---

### script13_tool_use.py

Extends previous scripts with Claude tool calling. When Claude responds with `stop_reason="tool_use"`,
the backend executes the requested tool, then sends the tool result back in a second API call 
so Claude can continue the response.

This is the tool-use *primitive* — single tool, two-turn flow. The agent loop (multi-step, multi-tool) is script 14.

**Key question:** Does Claude execute tools itself?
**Answer:** No. Claude only REQUESTS tool use. Backend owns execution, validation, and all real-world side effects.

**Key question:** Why is a second API call needed?
**Answer:** The first call pauses at the tool request. The second call continues the conversation after the backend sends the `tool_result` back to Claude.

**Key question:** Why include the full message history again?
**Answer:** Anthropic APIs are stateless. Every request must include the complete conversation state — user message, assistant tool request, and tool result.

---

## How to run

```bash
uvicorn script13_tool_use:app --reload
```

## Test with

Normal message (no tool use):

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello!"
  }'
```
output

```json
{"answer":"Hello! I'm doing well...","input_tokens":556,"output_tokens":35,"stop_reason":"end_turn"}
```

Trigger tool use:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What time is it right now?"
  }'
```

output

```json
{"answer":"The current time is **5:52 PM (17:52)** on **May 27, 2026** (UTC).","input_tokens":621,"output_tokens":32,"stop_reason":"end_turn"}
```