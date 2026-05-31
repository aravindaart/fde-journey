import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI, OpenAIError
import chromadb


load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path="./chroma_db")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")

menu_items = [
    "Classic Milk Tea - $4.50 - Black tea with milk and tapioca pearls",
    "Mango Milk Tea - $5.50 - Mango flavored milk tea with pearls",
    "Strawberry Smoothie - $6.00 - Fresh strawberry blended drink",
    "Taro Milk Tea - $5.00 - Creamy taro flavored milk tea",
    "Jasmine Green Tea - $4.00 - Light green tea without dairy",
    "Brown Sugar Boba - $6.50 - Brown sugar milk tea with extra pearls",
    "Lychee Fruit Tea - $5.25 - Refreshing lychee tea without dairy"
]

collection = chroma_client.get_or_create_collection(name="bubble_tea_menu")

if collection.count() == 0:

    embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=menu_items
    )

    embeddings = [
        item.embedding
        for item in embedding_response.data
    ]

    collection.add(
        documents=menu_items,
        embeddings=embeddings,
        ids=[f"menu_item_{i}" for i in range(len(menu_items))]
    )

    print("Menu ingested into ChromaDB.")

else:
    print("Menu already exists. Skipping ingestion.")

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)


class AskResponse(BaseModel):
    answer: str = Field(..., min_length=1)
    input_tokens: int
    output_tokens: int
    stop_reason: str


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        query_embedding_response = client.embeddings.create(input=[request.question], model="text-embedding-3-small")
        results = collection.query(query_embeddings=[query_embedding_response.data[0].embedding], n_results=3)
        retrieved_chunks = "\n".join(results["documents"][0])
        augmented_prompt = f"""
            Answer ONLY using the provided menu context.
            If the answer is not present in the context, say:
            "I could not find that in the menu."

            Menu Context:
            {retrieved_chunks}

            Customer Question:
            {request.question}
        """
        
        message = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": "Answer only from provided context."},
                {"role": "user", "content": augmented_prompt }
            ]
        )
        return AskResponse(answer=message.choices[0].message.content, input_tokens=message.usage.prompt_tokens, output_tokens=message.usage.completion_tokens, stop_reason=message.choices[0].finish_reason)
    except OpenAIError as e:
        raise HTTPException(status_code=503, detail=str(e))
