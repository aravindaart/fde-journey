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


### script17_embeddings.py

Introduces embeddings and semantic similarity search using OpenAI embeddings. Instead of keyword matching, the app converts text into vectors and compares meaning mathematically using cosine similarity.

Key question: Why use embeddings instead of string matching?
Answer: Embeddings capture semantic meaning, not exact words. "Mango drink with pearls" can match "Mango milk tea with tapioca pearls" even though the wording differs.

Key question: Why calculate cosine similarity?
Answer: Cosine similarity measures how close two vectors point in the same direction. Higher similarity means the texts are semantically more related.

Key question: Why request embeddings for [query] + menu in one API call?
Answer: Batch requests are more efficient than separate API calls. One network request generates embeddings for both the query and all menu items together.

## How to run

# OpenAI:

```bash
uvicorn script17_embeddings:app --reload
```

## Test with

```bash
curl -X POST http://localhost:8000/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "question": "I want a fruity bubble tea drink"
  }'
```

Output:

```json
{
  "answer": "Mango milk tea with tapioca pearls"
}
```

---

### script18_chromadb_intro.py

Introduces ChromaDB as a vector database for semantic search. Instead of manually generating embeddings and calculating cosine similarity, ChromaDB stores documents, generates embeddings internally, and performs similarity search automatically.

**Key question:** Why use a vector database instead of manual cosine similarity code?
**Answer:** A vector database handles embedding storage, indexing, and similarity search efficiently at scale. Manual cosine similarity works for learning but does not scale to large datasets.

**Key question:** Why does `collection.add()` require IDs?
**Answer:** IDs uniquely identify documents inside the collection. ChromaDB uses them for updates, retrieval, and deduplication behaviour.

**Key question:** Why does querying use `query_texts` instead of embeddings directly?
**Answer:** ChromaDB can automatically generate embeddings internally, so you can query using plain text without manually calling the embeddings API yourself.

---

## How to run

```bash
python script18_chromadb_intro.py
```

## Expected output

```json 
{'ids': [['1']], 'embeddings': None, 'documents': [['Mango milk tea with tapioca pearls']], 'uris': None, 'included': ['metadatas', 'documents', 'distances'], 'data': None, 'metadatas': [[{'source': 'menu'}]], 'distances': [[0.6898359060287476]]}
```
