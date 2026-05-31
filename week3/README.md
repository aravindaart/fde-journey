# Week 3 - OpenAI

## Scripts

### script15_openai_fastapi.py

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


### script16_provider_abstraction.py

Combines Anthropic and OpenAI into a single FastAPI app. The API contract stays identical while the backend dynamically switches providers using the LLM_PROVIDER environment variable.

Key question: Why move the provider logic into a separate call_llm() function?
Answer: It separates provider-specific SDK code from the FastAPI route. The route handles HTTP concerns; call_llm() handles LLM integration logic.

Key question: Why return the same AskResponse shape for both providers?
Answer: The API contract should stay stable even if the backend provider changes. Clients should not care whether the response came from OpenAI or Anthropic.

Key question: Why use an environment variable for provider selection?
Answer: Configuration belongs outside code. Switching providers via .env avoids code changes and redeploys for simple infrastructure/config updates.

## How to run

# Anthropic:

```bash
LLM_PROVIDER=anthropic uvicorn script16_provider_abstraction:app --reload
```

# OpenAI:

```bash
LLM_PROVIDER=openai uvicorn script16_provider_abstraction:app --reload
```

## Test with

Single turn:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain what FastAPI is."
  }'
```


