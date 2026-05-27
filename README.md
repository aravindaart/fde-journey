# From Frontend to Forward Deployed Engineer
### A 12-week public learning journal by Aravindhan Mohan

> "FDE roles sit at the intersection of software engineering,
> product thinking, and customer consulting. This repo documents
> my real transition — week by week, commit by commit."

---

## Who this is for

If you're a senior engineer with strong fundamentals but
zero hands-on AI experience, this roadmap is for you.

This is NOT a tutorial collection. This is a real journey
with real gaps, real mistakes, and real shipped projects.
Validated against live FDE job postings at OpenAI, Anthropic,
Arize AI, Google Cloud, Singtel, and Taxbit Singapore (May 2026).

---

## My starting point (May 2026)

- 10+ years frontend engineering (React, TypeScript, Redux)
- Principal consultant embedded at a large financial institution
- Python: can read, never written from scratch
- LLM APIs: never called one in code
- Deployed AI apps: zero

If that sounds like you — follow along.

---

## The 12-week roadmap

| Phase | Weeks | Focus | Key Output |
|-------|-------|-------|------------|
| 1 — Foundations | 1–3 | Python · Pydantic · FastAPI · First LLM API call | Deployed "Hello Agent" at a public URL |
| 2 — Applied AI | 4–6 | RAG · LangGraph · Evals · Docker | RAG demo + eval blog post + Dockerised app |
| 3 — Flagship | 7–9 | Full AI agent · MCP server · GCP · Observability | Bobasaur AI Concierge — live demo + case study |
| 4 — Job Sprint | 10–12 | Engineering write-up · Resume · 20+ applications | First FDE interview booked |

---

## What the flagship project is

**Bobasaur AI Concierge** — a WhatsApp-based AI ordering and
loyalty assistant for a real bubble tea business.

- RAG over menu, promotions, and FAQ
- Tool calls to a loyalty stamp database
- MCP server exposing loyalty operations
- Sends structured orders via WhatsApp/email
- Deployed on GCP Cloud Run
- Langfuse observability — cost, latency, tool success rate
- Eval suite measuring hallucination rate on menu items
- Production hardened: tests, CI, error handling, rate limits

This is not a tutorial chatbot. It serves real customers.

---

## Validated skill checklist

Cross-referenced against live Singapore FDE job postings
(OpenAI, Anthropic, Arize AI, Google Cloud, Singtel — May 2026):

| Skill | Required by | Status |
|-------|-------------|--------|
| Python | All postings | 🔨 Phase 1 |
| Pydantic (typed Python) | OpenAI, Anthropic | 🔨 Phase 1 Week 2 |
| FastAPI / Backend | All postings | 🔨 Phase 1 |
| LLM API (Anthropic + OpenAI) | All postings | 🔨 Phase 1 |
| RAG architecture | All postings | 🔨 Phase 2 |
| Tool use / Agents | All postings | 🔨 Phase 2 |
| LangGraph | Market standard 2026 | 🔨 Phase 2 Week 5 |
| Eval engineering | All postings | 🔨 Phase 2 Week 6 |
| Docker basics | Arize + Google | 🔨 Phase 2 Week 6 |
| MCP server | Anthropic explicitly | 🔨 Phase 3 Week 8 |
| GCP Cloud Run | Google + Arize | 🔨 Phase 3 Week 8 |
| Langfuse observability | OpenAI, Anthropic | 🔨 Phase 3 Week 9 |
| Production hardening | OpenAI explicitly | 🔨 Phase 3 Week 9 |
| TypeScript | Arize AI | ✅ Already have |
| Customer-facing delivery | All postings | ✅ Already have |
| Banking / regulated domain | Addepar, Palantir | ✅ Already have |
| Enterprise integration (SSO/OIDC) | OpenAI, Anthropic | ✅ Already have |

---

## Ground rules I set for myself

1. **No vibe coding.** Every line I commit, I can explain.
2. **Ship over perfect.** Ugly working code beats elegant
   unfinished code.
3. **Public accountability.** Weekly LinkedIn updates.
   No quiet weeks.
4. **Parking lot for distractions.** New ideas go in
   `parking-lot.md`, not into the plan.
5. **Understand before moving on.** If I can't explain it,
   I delete it and write it again.

---

## Weekly logs

| Week | Theme | Status |
|------|-------|--------|
| Week 0 | Setup — repo, Python, API key, tools | ✅ Done |
| Week 1 | Hello Agent — Python basics + FastAPI + deployed URL | ✅ Done |
| Week 2 | Conversational API · Streaming · Pydantic models | 🔨 In progress |
| Week 3 | OpenAI API + clean deployment to Render | ⏳ Upcoming |
| Week 4 | Embeddings + vector stores + first RAG | ⏳ Upcoming |
| Week 5 | Tool use + agents (raw) + LangGraph | ⏳ Upcoming |
| Week 6 | Eval engineering + Docker basics | ⏳ Upcoming |
| Week 7 | Flagship start — Bobasaur data + RAG layer | ⏳ Upcoming |
| Week 8 | Flagship build — tool calls + MCP server + GCP deploy | ⏳ Upcoming |
| Week 9 | Flagship polish — Langfuse + evals + production hardening + case study | ⏳ Upcoming |
| Week 10 | Engineering write-up — trade-offs, eval results, what broke | ⏳ Upcoming |
| Week 11 | Second project (MAS Banking RAG) if time + resume reframe | ⏳ Upcoming |
| Week 12 | Job sprint — 20+ applications + referrals | ⏳ Upcoming |

---

## Target companies (Singapore + APAC)

| Tier | Company | Why it fits |
|------|---------|-------------|
| A | Singtel FDE | Local enterprise, consulting background converts directly |
| A | **Arize AI** ⭐ | Singapore FDE open, 2–5 yrs exp, RAG + evals exact match |
| A | Databricks SG | Enterprise AI, strong fit |
| A | Genesys SG | Enterprise CX/AI, less competitive |
| B | ByteDance / BytePlus | High FDE volume in SG |
| B | Cohere SG | Agent-focused, matches Concierge story |
| B | BCG X Singapore | Hires consultant-engineers |
| B | Addepar SG | Financial services FDE, banking domain match |
| C | OpenAI Singapore | High bar (5+ yrs LLM), apply for interview reps |
| C | Anthropic SG | High bar, founding-team energy |
| C | Palantir Singapore | Original FDE company |

---

## Stack

Python · Pydantic · FastAPI · Anthropic Claude API · OpenAI API
LangGraph · ChromaDB · Docker · GCP Cloud Run · Langfuse · MCP
GitHub · VS Code

---

## Repo structure

```
fde-journey/
├── week1/          # Python warmups + Hello Agent
├── week2/          # Claude API + Pydantic
├── week3/          # OpenAI + Render deployment
├── week4/          # RAG demo
├── week5/          # Tool use + LangGraph agents
├── week6/          # Evals + Docker
├── week7-9/        # Bobasaur AI Concierge (flagship)
├── week10-11/      # Engineering write-up + second project
├── learnings.md    # Real unfiltered weekly notes
├── parking-lot.md  # Deferred ideas
└── README.md       # This file
```

---

## What's live

| Project | Stack | Status |
|---------|-------|--------|
| Week 1 — Hello Agent | FastAPI · Pydantic · Anthropic API | See repo to run locally |

To run locally:
```bash
cd week1
uvicorn script9_fastapi:app --reload
```

---

## Follow the journey

- LinkedIn: [aravindaart](https://www.linkedin.com/in/aravindaart/)
- Weekly updates posted every Sunday

---

## Want to follow this roadmap yourself?

Fork this repo. Start from Week 0.
The only rule that matters: understand every line you commit.

---

## Set up your own AI mentor

Want the same strict AI mentor system I'm using?

Download `fde-mentor-context.md` from this repo and follow the 4 steps inside:

1. Set up your daily doubts thread (Claude / ChatGPT / Gemini / any LLM)
2. Set up your weekly main mentor thread
3. Paste the mentor instructions into your AI tool
4. Fill in your details and start

Works with any AI tool. Free to use. Fork and adapt as you like.