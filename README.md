# Senior Engineer → AI Engineer in 12 Weeks

*A public roadmap and ground rules for senior engineers rebuilding their foundations in AI engineering — without vibe coding.*

A 12-week structure for going from "I've shipped a lot of production code with AI assistance" to "I can build, deploy, and defend an AI system end to end." Fork it, follow it, adapt it.

## Why this exists

If you're a senior engineer using Claude, ChatGPT, or Copilot every day, you've probably noticed the same thing: you're shipping code you can't always defend line by line. That's fine for CRUD apps. It is not fine for LLM systems, where the gap between "looks right" and "is right" is huge and silent.

This roadmap is for closing that gap on purpose, in public, with a real shipped project at the end.

**The one rule that matters: if you can't explain a line, rewrite it until you can.**

## Who this is for

- Senior engineers (5+ years) with strong fundamentals in any stack
- People who've used AI tools heavily and noticed the comprehension gap
- People who want to add AI engineering as a vertical, not pivot from scratch
- People willing to commit to ~10 hours/week for 12 weeks

This is **not** for:
- Beginners learning programming (the roadmap assumes you already know how to ship)
- People looking for a tutorial collection (this is structure, not lessons)
- People who want certificates (build a flagship and ship it — that's the certificate)

## The 12-week roadmap

| Phase | Weeks | Focus | What you ship |
|-------|-------|-------|---------------|
| 1 — Foundations | 1–3 | Language fundamentals · Typed data models · Web framework · First LLM API call | A deployed "Hello Agent" at a public URL |
| 2 — Applied AI | 4–6 | RAG · Agents · Evals · Containerisation | A RAG demo + eval results + Dockerised app |
| 3 — Flagship | 7–9 | Full AI system · Tool use · Deployment · Observability | Your flagship project — live, with users |
| 4 — Wrap | 10–12 | Engineering write-up · Portfolio polish · Reflection | Portfolio ready to share |

Each phase builds the layer below. Skip a phase and the next one collapses.

## Ground rules

1. **No vibe coding.** Every line you commit, you can explain. If you can't, rewrite it.
2. **Ship over perfect.** Ugly working code beats elegant unfinished code. Always.
3. **Public accountability.** Weekly update somewhere public (LinkedIn, blog, X). No quiet weeks.
4. **Parking lot for distractions.** New project ideas go in `parking-lot.md`, not into the plan. The plan is the plan.
5. **Keep a learnings log.** Real, unfiltered notes after every session. This is the most valuable artifact you'll produce — not the code. See [an example](https://github.com/aravindaart/fde-journey/blob/main/learnings.md).
6. **Understand before moving on.** If a concept doesn't click, stop and stay there. Speed comes from depth, not skipping.

## Pick your own flagship

Your Phase 3 flagship is the whole point of the roadmap. Everything in Phases 1 and 2 exists to make this project possible.

**What makes a good flagship:**

- **Real users.** Not a demo with synthetic data. Someone, somewhere, will actually use it.
- **Requires at least:** RAG + tool use + deployment. If it's only one of those, it's too small.
- **Measurable.** You can write evals that tell you whether it's working.
- **Shippable in 3 weeks** of focused work. Bigger than that and you'll spend Phase 4 still building instead of job hunting.
- **Showable in an interview.** No NDA, no licensing issues, no "I can't show you the code."

**Patterns that work:**

- An AI assistant for a small business in your network (cousin's restaurant, friend's clinic, your own side project)
- An internal tool for your current team that wouldn't get prioritised otherwise
- An AI layer on top of an existing project you own
- A specialised assistant for a hobby or community you're part of

**Patterns that don't:**

- Yet another generic chatbot with no specific domain
- A "platform" that does ten things shallowly
- Anything that depends on third-party data you don't have access to yet
- Projects you'll lose interest in by Week 9 (be honest with yourself about this)

Pick the flagship in Week 1. Don't wait until Phase 3. Knowing the destination shapes every script you write before then.

## Stack

This is an opinionated stack. Swap as you like, but pick something and commit by Week 1 — don't rotate stacks mid-roadmap.

**Phase 1:** Python · Pydantic · FastAPI · Anthropic or OpenAI SDK
**Phase 2:** A vector DB (ChromaDB / pgvector / Pinecone) · LangGraph or raw orchestration · Docker
**Phase 3:** A cloud platform (Render / GCP Cloud Run / Fly.io) · An observability tool (Langfuse / Helicone / LangSmith) · MCP if relevant to your flagship

Why Python: every LLM SDK ships Python first. Why FastAPI: Pydantic-native, type-driven, the cleanest fit for LLM APIs. Why an opinionated stack: optionality is paralysing in Week 1.

## Set up your own AI mentor

The roadmap works much better with a structured mentor system than with ad-hoc help.

**The setup:**

- **Daily doubts thread** — your debugging companion. Any LLM, fresh chat per topic. Burn it down weekly.
- **Weekly main mentor thread** — Sunday check-in. Tracks progress, calls out gaps, evolves the roadmap. Keep this thread alive for the full 12 weeks.

A mentor context file with full instructions and prompts is available [here](./fde-mentor-context.md). Download, fill in your details, paste into your LLM of choice.

## A real example

Someone is running this roadmap right now, in public, with full commit history and weekly updates. If you want to see what week-by-week execution actually looks like:

→ [JOURNEY.md](./JOURNEY.md) — one person's specific run of this roadmap, with their flagship, their target companies, and their weekly status.

## Planned repo structure

```
your-fde-journey/
├── week1/          # Foundations — language + first LLM call
├── week2/          # Web framework + typed data + streaming
├── week3/          # Second LLM provider + clean deploy
├── week4/          # Embeddings + vector store + first RAG
├── week5/          # Tool use + agents
├── week6/          # Evals + Docker
├── week7-9/        # YOUR FLAGSHIP project
├── week10-11/      # Engineering write-up + resume work
├── learnings.md    # Real unfiltered notes — the single most valuable file
├── parking-lot.md  # Deferred ideas
└── README.md       # This file
```

Create folders as you get to them. Don't pre-create Week 5 in Week 1.

## Fork and start

1. Fork this repo
2. Pick your flagship (Week 0)
3. Set up your mentor system
4. Start Week 1
5. Post your first weekly update by Sunday

The only rule that matters: understand every line you commit.