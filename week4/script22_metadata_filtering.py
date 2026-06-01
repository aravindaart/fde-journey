import os

from chromadb import PersistentClient
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
chroma_client = PersistentClient(path="./chroma_db")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
text = open("data/bubble_tea.txt").read()

collection = chroma_client.get_or_create_collection("bubble_tea")

metadata = {
    "SIGNATURE DRINKS": "menu",
    "PREMIUM CREATIONS": "menu",
    "SNACKS": "menu",
    "LOYALTY AND MEMBERSHIP": "policy",
    "ORDERING AND OPERATIONS": "operations",
}

sections = list(filter(lambda s: s.strip(), text.split("---")))


def ingest_with_metadata(text: str, doc_type: str, chunk_size: int, overlap: int):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append((chunk, {"type": doc_type}))
        start += chunk_size - overlap
    return chunks


def ingest_sections(sections: list[str]):
    sections_by_type = {}
    for section in sections:
        section_name = section.split("\n\n")[1].strip()
        doc_type = metadata.get(section_name, "operations")
        if doc_type not in sections_by_type:
            sections_by_type[doc_type] = []
        sections_by_type[doc_type].append(section)

    for doc_type, doc_sections in sections_by_type.items():
        text_block = "\n\n".join(doc_sections)
        chunks_with_meta = ingest_with_metadata(text_block, doc_type, chunk_size=200, overlap=50)
        chunks, metadatas = map(list, zip(*chunks_with_meta))
        embeddings = openai_client.embeddings.create(input=chunks, model="text-embedding-3-small").data
        collection.add(
            documents=chunks,
            embeddings=[e.embedding for e in embeddings],
            metadatas=metadatas,
            ids=[f"{doc_type}_chunk_{i}" for i in range(len(chunks))]
        )


if collection.count() == 0:
    ingest_sections(sections)


def retrieve_filtered(query_embedding: list[float], doc_type: str, n_results: int) -> list[str]:
    results = collection.query(query_embeddings=[query_embedding], where={"type": doc_type}, n_results=n_results)
    return results["documents"][0]


def retrieve_unfiltered(query_embedding: list[float], n_results: int) -> list[str]:
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    return results["documents"][0]


queries = [
    ("what snacks are available", "menu"),
    ("how do reward points expire", "policy"),
]

query_embeddings = openai_client.embeddings.create(input=[q[0] for q in queries], model="text-embedding-3-small").data

for (query, doc_type), query_embedding in zip(queries, query_embeddings):
    print(f"\nQuery: {query} | Doc Type: {doc_type}")
    print("Filtered Retrieval:")
    filtered_results = retrieve_filtered(query_embedding.embedding, doc_type, n_results=2)
    for res in filtered_results:
        print(f"- {res}")

    print("\nUnfiltered Retrieval:")
    unfiltered_results = retrieve_unfiltered(query_embedding.embedding, n_results=2)
    for res in unfiltered_results:
        print(f"- {res}")