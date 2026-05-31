# Week 3 - OpenAI

## Scripts

script15_openai_fastapi.py

Ports the earlier Claude FastAPI app to OpenAI's Ask Completions API. The overall architecture stays the same - FastAPI + Pydantic + LLM API - but the SDK shape and response structure differ between Anthropic and OpenAI.

Key question: Why does OpenAI need a "system" message while the earlier Claude example didn't?
Answer: Anthropic has a dedicated system= parameter at the top level of the API call, so the system prompt never goes in the messages array. OpenAI has no such parameter - the system prompt goes inside the messages array as {"role": "system", ...}. Same concept, different API design choice.

Key question: Why is the response access different between Claude and OpenAI?
Answer: OpenAI returns completions inside choices[], while Anthropic returns structured content blocks in content[]. Different SDKs, different response contracts.

Key question: Why does OpenAI return responses inside a choices array even for a single completion?
Answer: The API is designed to support multiple generated completions in one request, so responses are always wrapped in choices[] even when only one answer is returned.

## How to run

```bash
uvicorn script15_openai_fastapi:app --reload
```

## Test with

Single turn:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is FastAPI?"
  }'
```