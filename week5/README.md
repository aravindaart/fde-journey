# Week 5 - Evals, Observability & Agentic Frameworks

## Scripts

### script24_evals.py

Introduces a simple evaluation framework for a tool-routed RAG agent. The script runs a set of predefined test cases and measures performance across three stages of the pipeline: tool routing, retrieval quality, and answer quality.

**Key question:** Why evaluate routing, retrieval, and answers separately?
**Answer:** Failures can occur at different stages of the RAG pipeline. Separating the metrics makes it easier to identify whether a problem comes from tool selection, retrieval, or answer generation.

**Key question:** Why check retrieved chunks before checking answers?
**Answer:** Retrieval is the foundation of RAG. If the correct information is not retrieved, answer failures are often retrieval failures rather than model failures.

**Key question:** Why use expected keywords instead of manual inspection?
**Answer:** Keyword checks provide a simple and repeatable way to evaluate behaviour across multiple test cases without manually reviewing every run.

---

## How to run

```bash
python script24_evals.py
```

## Example test cases

```text
- What time does Bubble Tea Lab close on Saturday?
- Does the Galactic Pistachio drink contain nuts?
- Can I redeem points for the Fossil Praline Crunch Shake?
- How many points do I have?
- What is the status of order BT123?
```

## Expected behaviour

* Knowledge questions should route to `search_knowledge_base`
* Loyalty questions should route to `get_loyalty_points`
* Order questions should route to `get_order_status`
* Retrieved chunks should contain the expected supporting information
* Final answers should contain the expected information

## Metrics reported

```text
Summary:
Routing Passes: 3/5
Chunk Passes: 2/5
Answer Passes: 2/5
```

## Failure modes observed

**Routing failure:** The agent selects the wrong tool for the user's question, preventing the correct information source from being used.

**Retrieval failure:** The correct tool is selected but the retrieved chunks do not contain the expected information.

**Grounding failure:** The correct chunk is retrieved but the final answer does not correctly use the retrieved information.

**Hallucinated success:** The retrieved chunk is incorrect or missing information, but the model still produces a seemingly correct answer from its own knowledge.

---

### script25_llm_judge_eval.py

Introduces an LLM-as-a-Judge evaluation framework for a tool-routed RAG agent. The script runs a set of predefined test cases, generates answers using tool calls and retrieval, and then uses a separate judge model to evaluate whether the answers are grounded in the retrieved context and relevant to the user's question.

**Key question:** Why use a judge model instead of keyword matching?
**Answer:** A judge model can evaluate answer quality more holistically, checking whether answers are supported by retrieved context and whether they directly address the user's question.

**Key question:** Why evaluate groundedness and relevance separately?
**Answer:** An answer may be relevant but contain hallucinated information, or it may be grounded in retrieved context but fail to answer the user's question. Separating these metrics helps identify the specific failure mode.

**Key question:** Why only measure groundedness when retrieval is used?
**Answer:** Groundedness can only be evaluated against retrieved context. Questions answered using non-retrieval tools such as loyalty points or order status do not have retrieved documents to compare against.

---

## How to run

```bash
python script25_llm_judge_eval.py
```

## Example test cases

```text
- What time does Bubble Tea Lab close on Saturday?
- Does the Galactic Pistachio drink contain nuts?
- Can I redeem points for the Fossil Praline Crunch Shake?
- How many points do I have?
- What is the status of order BT123?
```

## Expected behaviour

```text
The agent should select the appropriate tool for each question
Knowledge-base questions should call search_knowledge_base
Loyalty questions should call get_loyalty_points
Order questions should call get_order_status
Retrieved context should support the generated answer
The judge should evaluate whether answers are grounded and relevant
```

## Metrics reported

```text
Summary:
Grounded Passes: 2/2
Relevant Passes: 3/5
Grounded Eligible: 2/5
```

## Failure modes observed

**Tool selection failure:** The agent calls the wrong tool or fails to call the appropriate tool for the user's question.

**Retrieval failure:** The correct tool is selected but the retrieved context does not contain the information needed to answer the question.

**Grounding failure:** The answer includes information that is not supported by the retrieved context.

**Relevance failure:** The answer is grounded but does not directly answer the user's question.

**Hallucinated success:** The judge scores an answer as grounded and relevant even though it is wrong or unsupported — the eval reports a pass while the underlying answer is actually a failure. More dangerous than a visible failure because nothing in the metrics flags it.

**Judge non-determinism:** Re-running the same test case can produce different verdicts. The Fossil Praline redemption case was judged grounded in one run and not grounded in another, with no change to the underlying code or data — a real limitation of LLM-as-judge versus deterministic keyword matching.

---

### script26_observability.py

Introduces Langfuse tracing into a tool-routed RAG agent. The script instruments LLM calls, retrieval operations, and tool executions, allowing the entire workflow to be visualized as a trace in Langfuse.

**Key question:** Why use Langfuse observability?
**Answer:** Observability makes it easier to understand how the agent arrives at an answer by showing LLM calls, retrieval operations, tool usage, and execution flow in a single trace.

**Key question:** Why trace retrieval and tools separately?
**Answer:** Retrieval and tools perform different roles in the agent workflow. Separate spans make it easier to identify whether issues come from retrieval, tool execution, or answer generation.

**Key question:** Why add metadata to tool spans?
**Answer:** Metadata provides additional execution details such as whether a lookup completed successfully, making debugging and monitoring easier.

---

## How to run

```bash
python script26_observability.py
```

## Example queries

```text
- What's my order status for order #42?
- What snacks are available?
- How do reward points expire?
```

## Expected behaviour

* A trace is created for each user query
* Claude API calls appear as generation spans
* Knowledge base searches appear as retriever spans
* Loyalty point lookups appear as tool spans
* Order status lookups appear as tool spans
* Tool spans contain lookup metadata

## Observability captured

```text
call_llm
├── call_claude
├── get_order_status
└── call_claude
```

## Engineering findings

**Generation span placement:** Decorators execute once per function call. Because `call_llm()` is invoked once and contains the internal tool loop, a generation decorator on that function cannot create per-iteration generation spans. Moving the generation decorator to `call_claude()` creates one generation span for each Claude API call.

**PII-safe tool tracing:** Tool spans disable automatic input and output capture to avoid recording customer identifiers and lookup results. Operational status is recorded through manually attached span metadata instead.

**Environment compatibility:** Langfuse setup required resolving Python-version and virtual-environment dependency conflicts before instrumentation could be tested successfully.

---

### script27_langgraph.py

Introduces LangGraph by building a simple agent workflow using nodes, edges, and shared state. The script demonstrates how LangGraph manages execution flow while maintaining conversation history across LLM and tool calls.

**Key question:** Why use LangGraph?
**Answer:** LangGraph simplifies building multi-step AI workflows by managing execution flow, shared state, and routing between nodes instead of requiring custom control logic.

**Key question:** What are nodes, edges, and state?
**Answer:** Nodes perform work, edges determine the next step, and state stores the shared data passed between nodes.

---

## How to run

```bash
python script27_langgraph.py
```

## Example queries

```text
- What's my order status for order #42?
- What snacks are available?
- How do reward points expire?
```

## Expected behaviour

* A LangGraph workflow executes from start to finish
* Conversation history is preserved across nodes
* Tools are called when required
* The final response is returned after all graph execution completes

## Graph flow

```text
START
  │
  ▼
call_llm
  │
  ├── stop_reason == "tool_use" ──► execute_tools ──► call_llm (loop back)
  │
  └── stop_reason == "end_turn" ──► END
```

## Engineering findings

**Message state:** Without a reducer, LangGraph replaces state fields on each node return. Both `call_llm` and `execute_tools` return the full updated `messages` list — existing history plus the new message appended.

**Naming collisions:** Reusing the name `tools` for both a tool list and a graph node caused Python name shadowing. Using distinct names (for example, `tools_list` and `execute_tools`) avoids this issue.

**State serialization:** Pydantic objects returned in message content needed `model_dump()` before being stored in graph state, ensuring the state remains serializable.
