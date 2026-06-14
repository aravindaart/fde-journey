# Week 4 - RAG

## Scripts

### script20_chunk_retrieval_comparison.py

Extends the earlier chunking experiment by embedding both fixed-size chunks and overlapping chunks into separate ChromaDB collections, then comparing retrieval quality across real semantic queries.

**Key question:** Why compare retrieval results instead of just inspecting chunks manually?
**Answer:** Good-looking chunks do not guarantee good retrieval. The real test is which chunks semantic search actually retrieves for user queries.

**Key question:** Why create separate ChromaDB collections for fixed and overlapping chunks?
**Answer:** Separate collections isolate the retrieval strategies so their behaviour can be compared independently using the same queries and embeddings.

**Key question:** Why can retrieval still fail even with overlap?
**Answer:** Embedding similarity optimises for semantic closeness, not answer completeness. The most semantically similar chunk may still miss the exact detail needed to answer the question.

---

## How to run

```bash
python script20_chunk_retrieval_comparison.py
```

## Example queries tested

```text
- how much is the Galactic Pistachio drink
- what snacks are available
- do customers earn any rewards
```

## Expected behaviour

* Fixed chunks may split important information across chunk boundaries.
* Overlapping chunks usually improve retrieval quality.
* Retrieval can still return incomplete chunks even when a better chunk exists nearby.

## Reset

Delete `./chroma_db` to force re-embedding if the source document or chunk size changes.

---

### script21_rag_failure_modes.py

Builds a more realistic RAG evaluation pipeline by testing difficult multi-part customer queries against retrieved chunks and analysing where the system fails. The script demonstrates two distinct RAG failure modes: retrieval misses and grounding failures.

**Key question:** Why test with complicated multi-part questions instead of simple queries?
**Answer:** Real users ask compound questions spanning multiple facts. These queries stress retrieval quality, chunking strategy, and grounding reliability much harder than simple keyword lookups.
**Key question:** Why strengthen the system prompt with strict grounding instructions?
**Answer:** Retrieval alone does not prevent hallucinations. The LLM must also be explicitly instructed to answer only from retrieved context and admit when information is missing.
**Key question:** Why can the system still fail even with a strong prompt?
**Answer:** The LLM cannot answer information that retrieval never provided. Prompting can reduce hallucinations but cannot fix missing context.

---

## How to run

```bash
python script21_rag_failure_modes.py
```

## Example queries tested

```text
- Can I get the Galactic Pistachio drink in the morning and is it safe for nut allergies?
- How do reward points expire and can I use them for the Fossil Praline Shake?
- What time does Bobasaur close on weekends during school holidays and when is last order?
- I want Jurassic Fries with cheese — what does it cost and are they gluten free?
- Can I order Mango Comet Splash with no sugar and get it delivered to Clementi?
```

## Expected behaviour
- Some answers will be correct and grounded.
- Some answers will partially fail because critical context was split across chunk boundaries.
- Some answers may hallucinate despite explicit grounding instructions.

## Failure modes observed

**Retrieval miss:** The correct information existed in the document but was split across a chunk boundary. The relevant chunk was not included in top-k results so the LLM never received it.

**Grounding failure:** The LLM generated a confident answer using its own training knowledge instead of the retrieved context, rather than saying it didn't know.

A stronger system prompt reduced grounding failures but cannot fix retrieval misses.

---

### script22_metadata_filtering.py

Introduces metadata-aware retrieval in ChromaDB. Instead of searching across all chunks equally, documents are tagged by category (`menu`, `policy`, `operations`) and retrieval is filtered using metadata constraints.

**Key question:** Why add metadata to chunks?
**Answer:** Metadata lets retrieval stay within the correct document category, reducing semantically related but contextually wrong results.

**Key question:** Why can unfiltered retrieval return incorrect chunks even when semantic similarity works?
**Answer:** Semantic similarity only measures relatedness. A chunk mentioning "snacks" in a loyalty policy can outrank an actual menu chunk because embeddings do not understand business intent or document structure.

**Key question:** Why did filtering fix the reward points retrieval issue from script21?
**Answer:** The relevant chunks were correctly tagged as `policy`, so retrieval searched only within policy-related chunks instead of the entire document space.

---

## How to run

```bash
python script22_metadata_filtering.py
```

## Example queries tested

```text
- what snacks are available
- how do reward points expire
```

## Expected behaviour

* Filtered retrieval keeps results inside the correct document category.
* Unfiltered retrieval may return semantically related but contextually incorrect chunks.
* Metadata filtering improves retrieval precision by narrowing the search space.

---

### script23_tool_routing_rag.py

Builds a tool-routed RAG assistant where Claude decides which backend tool to call based on the user's request. The system combines operational tools (`get_order_status`) with metadata-filtered RAG retrieval (`search_knowledge_base`) inside a single agent workflow.

**Key question:** Why split functionality into multiple tools instead of one giant prompt?
**Answer:** Different tasks require different systems. Operational actions (order lookup) and semantic retrieval (knowledge base search) have different inputs, outputs, and logic.

**Key question:** Why include `doc_type` in the retrieval tool?
**Answer:** Metadata filtering constrains retrieval to the correct category (`menu`, `policy`, etc.), reducing cross-contamination between unrelated chunks.

**Key question:** Why does Claude sometimes rewrite the user's search query?
**Answer:** The model acts as a retrieval client and optimises the search query semantically, often generating better retrieval terms than the raw user input.

---

## How to run

```bash
python script23_tool_routing_rag.py
```

## Example queries tested

```text
- What's the status of order 42?
- What snacks are available?
- How do reward points expire?
```

## Expected behaviour

* Order questions route to `get_order_status`
* Knowledge questions route to `search_knowledge_base`
* Retrieval is filtered using metadata categories like `menu` and `policy`

---

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
