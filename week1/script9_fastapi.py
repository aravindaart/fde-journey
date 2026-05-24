import os

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field


load_dotenv()
app = FastAPI()
client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class AskResponse(BaseModel):
    answer: str = Field(..., min_length=1)


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": request.question }
        ]
    )
    return AskResponse(answer=message.content[0].text)