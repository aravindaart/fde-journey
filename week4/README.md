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
