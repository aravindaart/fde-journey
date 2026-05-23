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
Validated against live FDE job postings at OpenAI, Arize AI,
and Google Cloud Singapore (May 2026).

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
| 1 — Foundations | 1–3 | Python · FastAPI · First LLM API call | Deployed "Hello Agent" at a public URL |
| 2 — Applied AI | 4–6 | RAG · Tool use · Evals · Docker basics | RAG demo + eval blog post + Dockerised app |
| 3 — Flagship | 7–9 | Full AI agent · Real users · GCP Cloud Run | Bobasaur AI Concierge — live demo + case study |
| 4 — Job Sprint | 10–12 | 2nd project · Resume · 20+ applications | First FDE interview booked |

---

## What the flagship project is

**Bobasaur AI Concierge** — a WhatsApp-based AI ordering and
loyalty assistant for a real bubble tea business.

- RAG over menu, promotions, and FAQ
- Tool calls to a loyalty stamp database
- Sends structured orders via WhatsApp/email
- Deployed on GCP Cloud Run
- Eval suite measuring hallucination rate on menu items

This is not a tutorial chatbot. It serves real customers.

---

## Validated skill checklist

Cross-referenced against live Singapore FDE job postings
(OpenAI, Arize AI, Google Cloud — May 2026):

| Skill | Required by | Status |
|-------|-------------|--------|
| Python | All 3 postings | 🔨 Phase 1 |
| FastAPI / Backend | Implied by all | 🔨 Phase 1 |
| LLM API (Anthropic + OpenAI) | All 3 postings | 🔨 Phase 1 |
| RAG architecture | All 3 explicitly | 🔨 Phase 2 |
| Tool use / Agents | All 3 explicitly | 🔨 Phase 2 |
| Eval engineering | All 3 explicitly | 🔨 Phase 2 |
| Docker basics | Arize + Google | 🔨 Phase 2 |
| GCP Cloud Run deployment | Google + Arize | 🔨 Phase 3 |
| TypeScript | Arize AI | ✅ Already have |
| Customer-facing delivery | All 3 postings | ✅ Already have |
| Project management | All 3 postings | ✅ Already have |
| Banking / regulated domain | Addepar + Palantir | ✅ Already have |

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
| Week 1 | Hello Agent — Python basics + FastAPI + deployed URL | 🔨 In progress |
| Week 2 | Claude API deep dive + environment variables + error handling | ⏳ Upcoming |
| Week 3 | Wrap up foundations + add OpenAI API + deploy cleanly | ⏳ Upcoming |
| Week 4 | Embeddings + vector stores + first RAG | ⏳ Upcoming |
| Week 5 | Tool use + function calling + agents | ⏳ Upcoming |
| Week 6 | Eval engineering + Docker basics | ⏳ Upcoming |
| Week 7 | Flagship start — Bobasaur data + RAG layer | ⏳ Upcoming |
| Week 8 | Flagship build — tool calls + WhatsApp + GCP deploy | ⏳ Upcoming |
| Week 9 | Flagship polish — evals + case study + LinkedIn post | ⏳ Upcoming |
| Week 10 | Second project start (MAS Banking RAG) | ⏳ Upcoming |
| Week 11 | Second project complete + resume reframe | ⏳ Upcoming |
| Week 12 | Job sprint — 20+ applications + referrals | ⏳ Upcoming |

---

## Target companies (Singapore + APAC)

| Company | Why it fits |
|---------|-------------|
| **Arize AI** (top pick) | Singapore FDE role open, 2–5 yrs exp, RAG + evals focus |
| OpenAI Singapore | High bar (5+ yrs AI), apply in Week 12 |
| Google Cloud FDE | Actively hiring Singapore FDE II–IV right now |
| Addepar Singapore | Financial services FDE — banking domain match |
| Palantir Singapore | Original FDE company, likes domain experts |
| BCG X Singapore | Hires consultant-engineers, strong culture fit |

---

## Stack

Python · FastAPI · Anthropic Claude API · OpenAI API
Docker · GCP Cloud Run · ChromaDB · GitHub · VS Code

---

## Repo structure

```
fde-journey/
├── week1/          # Python warmups + Hello Agent
├── week2/          # Claude API scripts
├── week3/          # OpenAI + clean deployment
├── week4/          # RAG demo
├── week5/          # Tool use / agents
├── week6/          # Evals + Docker
├── week7-9/        # Bobasaur AI Concierge (flagship)
├── week10-11/      # Second project
├── learnings.md    # Real unfiltered weekly notes
├── parking-lot.md  # Deferred ideas
└── README.md       # This file
```

---

## Follow the journey

- LinkedIn: [aravindaart](https://www.linkedin.com/in/aravindaart/)
- Weekly updates posted every Sunday

---

## Want to follow this roadmap yourself?

Fork this repo. Start from Week 0.
The only rule that matters: understand every line you commit.