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
