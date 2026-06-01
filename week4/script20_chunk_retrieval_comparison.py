import os

import chromadb
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path="./chroma_db")


fixed_collection = chroma_client.get_or_create_collection("fixed_chunks")
overlap_collection = chroma_client.get_or_create_collection("overlap_chunks")


def embed_and_store(collection, chunks: list[str], prefix: str):
    embeddings = openai_client.embeddings.create(input=chunks, model="text-embedding-3-small").data
    collection.add(
        documents=chunks,
        embeddings=[e.embedding for e in embeddings],
        ids=[f"{prefix}_chunk_{e.index}" for e in embeddings]
    )


def chunk_fixed(text: str, chunk_size: int) -> list[str]:
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def chunk_with_overlap(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


text = open("data/source_document.txt").read()

fixed = chunk_fixed(text, chunk_size=200)
overlapping = chunk_with_overlap(text, chunk_size=200, overlap=50)

print(f"Fixed chunks: {len(fixed)}")
for i, chunk in enumerate(fixed):
    print(f"\n--- Chunk {i} ---\n{chunk}")

print(f"\nOverlapping chunks: {len(overlapping)}")
for i, chunk in enumerate(overlapping):
    print(f"\n--- Chunk {i} ---\n{chunk}")

# Guard prevents re-embedding on restart but will serve stale data
# if source document or chunk_size changes. Delete ./chroma_db to reset.
if fixed_collection.count() == 0:
    print("Embedding and storing fixed chunks...")
    embed_and_store(fixed_collection, fixed, "fixed")

if overlap_collection.count() == 0:
    print("Embedding and storing overlapping chunks...")
    embed_and_store(overlap_collection, overlapping, "overlap")


queries = [
    "how much is the Galactic Pistachio drink",
    "what snacks are available",
    "do customers earn any rewards",
]

query_embeddings = openai_client.embeddings.create(input=queries, model="text-embedding-3-small").data

for query, query_embedding in zip(queries, query_embeddings):
    print(f"\nQuery: {query}")
    for collection in [fixed_collection, overlap_collection]:
        results = collection.query(query_embeddings=[query_embedding.embedding], n_results=1)
        retrieved_chunk = results["documents"][0][0] if results["documents"][0] else "No chunk found"
        print(f"Collection: {collection.name}, Retrieved Chunk: {retrieved_chunk}")