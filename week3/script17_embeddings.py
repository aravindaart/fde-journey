import os
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
bubble_tea_menu = [
    "Mango milk tea with tapioca pearls",
    "Mango smoothie with lychee jelly",
    "Quarterly financial report Q3"
]


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)


class AskResponse(BaseModel):
    answer: str = Field(..., min_length=1)
    

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_most_similar_menu_item(query, menu):
    similarities = []
    embeddings = client.embeddings.create(input=[query] + menu, model="text-embedding-3-small").data
    query_embedding = embeddings[0].embedding
    menu_embeddings = embeddings[1:]
    for menu_item, menu_item_embedding in zip(menu, menu_embeddings):
        similarity = cosine_similarity(query_embedding, menu_item_embedding.embedding)
        similarities.append((similarity, menu_item))
    similarities.sort(reverse=True)
    return similarities[0][1]


@app.post("/suggest", response_model=AskResponse)
def suggest(request: AskRequest) -> AskResponse:
    try:
        most_similar_item = find_most_similar_menu_item(request.question, bubble_tea_menu)
        return AskResponse(answer=most_similar_item)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))