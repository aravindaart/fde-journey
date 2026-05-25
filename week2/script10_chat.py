import os

from typing import Literal
from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


load_dotenv()
app = FastAPI()
client = Anthropic(api_key=os.getenv(“ANTHROPIC_API_KEY”))
SYSTEM_PROMPT = os.getenv(“SYSTEM_PROMPT”, “You are a helpful assistant.”)


class MessageBody(BaseModel):
    role: Literal[“user”, “assistant”]
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    messages: list[MessageBody]


class ChatResponse(BaseModel):
    answer: str = Field(..., min_length=1)
    input_tokens: int
    output_tokens: int
    stop_reason: Literal[“end_turn”,“max_tokens”,“stop_sequence”,“tool_use”,“pause_turn”,“refusal”]


@app.post(”/chat”, response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        message = client.messages.create(
            model=“claude-haiku-4-5-20251001”,
            max_tokens=1024,
            messages=[message.model_dump() for message in request.messages],
            system=SYSTEM_PROMPT
        )
        return ChatResponse(
            answer=message.content[0].text,
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
            stop_reason=message.stop_reason
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))