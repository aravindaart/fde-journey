# My FDE Journey

*One person's specific run of the [Senior Engineer → AI Engineer in 12 Weeks](./README.md) roadmap.*

This file documents my actual execution of the roadmap — starting point, flagship plan, weekly progress, and what's live. If you're considering forking the repo, this is what week-by-week reality looks like.

## Starting point (May 2026)

- 10+ years frontend engineering (React, TypeScript, Redux)
- Backend experience with Node.js
- Principal consultant embedded at a large Singapore financial institution
- Python: written small scripts before, never built a production backend in it
- LLM APIs: never called one in code
- Deployed AI apps: zero

## My planned flagship

*Phase 3 build target. Currently in Week 3 of foundations — flagship construction starts Week 7. Project name and full details to be added when Phase 3 begins.*

A WhatsApp-based AI ordering and loyalty assistant for a real small business.

Planned scope:

- RAG over the business catalog, promotions, and FAQ
- Tool calls to a loyalty stamp database
- MCP server exposing loyalty operations
- Sends structured orders via WhatsApp/email
- Deployed on GCP Cloud Run
- Langfuse observability — cost, latency, tool success rate
- Eval suite measuring hallucination rate on catalog items
- Production-hardened: tests, CI, error handling, rate limits

This will not be a tutorial chatbot. It will serve real customers.

## Why this flagship fits the criteria

Evaluated against the [flagship criteria](./README.md#pick-your-own-flagship):

- ✅ Real users — a working small business with real customers and a defined catalog
- ✅ Requires RAG + tool use + deployment — all three are core to the design
- ✅ Measurable — catalog hallucination rate is a clean eval surface
- ✅ Shippable in 3 weeks — scope is locked: WhatsApp interface only, no POS or third-party platform integrations (those are in `parking-lot.md`)
- ✅ Showable — no NDA, can demo openly

## Skills I'm building

| Skill | Status |
|-------|--------|
| Python fundamentals | ✅ Done (Week 1) |
| FastAPI / Backend | ✅ Done (Week 1) |
| Pydantic (typed data models) | ✅ Done (Week 1–2) |
| Anthropic API | ✅ Done (Week 1) |
| Streaming responses | ✅ Done (Week 2) |
| Conversational memory | ✅ Done (Week 2) |
| Context management (sliding window) | ✅ Done (Week 2) |
| Tool use / Agents (raw) | ✅ Done (Week 2) |
| OpenAI API | 🔨 Week 3 |
| RAG architecture | ⏳ Phase 2 |
| LangGraph | ⏳ Phase 2 Week 5 |
| Eval engineering | ⏳ Phase 2 Week 6 |
| Docker basics | ⏳ Phase 2 Week 6 |
| MCP server | ⏳ Phase 3 Week 8 |
| GCP Cloud Run | ⏳ Phase 3 Week 8 |
| Langfuse observability | ⏳ Phase 3 Week 9 |
| Production hardening | ⏳ Phase 3 Week 9 |
| TypeScript | ✅ Already have |
| Customer-facing delivery | ✅ Already have |
| Banking / regulated domain | ✅ Already have |
| Enterprise integration (SSO/OIDC) | ✅ Already have |

## Weekly logs

| Week | Theme | Status | Details |
|------|-------|--------|---------|
| Week 0 | Setup — repo, Python, API key, tools | ✅ Done | — |
| Week 1 | Hello Agent — Python basics + FastAPI + deployed URL | ✅ Done | [`week1/`](./week1) |
| Week 2 | Conversational API · Streaming · Context management · Tool use · Agent loop | ✅ Done | [`week2/`](./week2) |
| Week 3 | OpenAI API + provider abstraction | 🔨 In progress | — |
| Week 4 | Embeddings + vector stores + first RAG | ⏳ Upcoming | — |
| Week 5 | LangGraph — build raw first, then with framework | ⏳ Upcoming | — |
| Week 6 | Eval engineering + Docker basics | ⏳ Upcoming | — |
| Week 7 | Flagship start — business data ingestion + RAG layer | ⏳ Upcoming | — |
| Week 8 | Flagship build — tool calls + MCP server + GCP deploy | ⏳ Upcoming | — |
| Week 9 | Flagship polish — Langfuse + evals + production hardening + case study | ⏳ Upcoming | — |
| Week 10 | Engineering write-up — trade-offs, eval results, what broke | ⏳ Upcoming | — |
| Week 11 | Second project (MAS Banking RAG) if time + portfolio refresh | ⏳ Upcoming | — |
| Week 12 | Engineering write-up + portfolio polish | ⏳ Upcoming | — |

## Selected learnings so far

The full unfiltered log is in [`learnings.md`](./learnings.md). A few of the sharper ones:

> Worst class of bug: returns wrong data without crashing, erroring, or logging. Truncated LLM output falls into this class. Defensive engineering = surfacing the metadata that lets you detect it.

> Tool execution is fully controlled by the backend. The LLM can request tools, but only your server can safely execute functions, APIs, databases, or external actions.

> tool_use is not agentic — it's a message type. The agent loop is what's agentic. Anthropic gives you the primitive; your code decides what to do with it.

> The loop is what makes it agentic. Claude passes one tool's output as the next tool's input by itself — the loop enables data flow between tools that a hardcoded flow can't do.

> Multi-tool agent loops need an iteration cap to prevent infinite tool-calling loops. Exiting due to max iterations is a controlled failure case, not a successful completion.

> Before reusing code from a previous script, check that the data shape matches. Pattern: when reusing code, ask "is the input here the same type as it was there?"

## What's live

*Live links added as projects are deployed.*

To run locally:
```bash
cd week1
uvicorn script9_fastapi:app --reload
```

## Follow along

- LinkedIn: [aravindaart](https://www.linkedin.com/in/aravindaart/)
- Weekly updates posted every Sunday