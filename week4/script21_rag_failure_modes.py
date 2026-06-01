import os

from openai import OpenAI
from dotenv import load_dotenv
from anthropic import Anthropic
from chromadb import PersistentClient


load_dotenv()
chroma_client = PersistentClient(path="./chroma_db")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
text = open("data/bubble_tea.txt").read()
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a Bobasaur Tea Lab assistant. "
    "Answer questions strictly using the context provided below. "
    "Do not use any knowledge outside the context. "
    "If the context contains a partial answer, state what you found and explicitly say the rest is not available in the provided information. "
    "If the context contains no relevant information, say exactly: I don't have that information."
)

collection = chroma_client.get_or_create_collection("menu_chunks")


def embed_and_store(chunks: list[str], prefix: str):
    embeddings = openai_client.embeddings.create(input=chunks, model="text-embedding-3-small").data
    collection.add(
        documents=chunks,
        embeddings=[e.embedding for e in embeddings],
        ids=[f"{prefix}_chunk_{e.index}" for e in embeddings]
    )


def retrieve(query_embedding: list[float], n_results: int) -> list[str]:
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    return results["documents"][0]


def answer(query: str, chunks: list[str]) -> str:
    context = "\n".join(chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    message = claude_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": prompt }
        ]
    )
    return message.content[0].text


def overlap_chunk(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


chunks = overlap_chunk(text, chunk_size=200, overlap=50)

if collection.count() == 0:
    print("Embedding and storing chunks...")
    embed_and_store(chunks, "menu")

queries = [
    "Can I get the Galactic Pistachio drink in the morning and is it safe for nut allergies?",
    "How do reward points expire and can I use them for the Fossil Praline Shake?",
    "What time does Bobasaur close on weekends during school holidays and when is last order?",
    "I want Jurassic Fries with cheese — what does it cost and are they gluten free?",
    "Can I order Mango Comet Splash with no sugar and get it delivered to Clementi?",
]

query_embeddings = openai_client.embeddings.create(input=queries, model="text-embedding-3-small").data

for query, embedding in zip(queries, query_embeddings):
    retrieved_chunks = retrieve(embedding.embedding, 3)
    print(f"\nQuery: {query}\nRetrieved Chunks: {retrieved_chunks}")
    answer_text = answer(query, retrieved_chunks)
    print(f"Answer: {answer_text}")

