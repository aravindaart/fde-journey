import os

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field


load_dotenv()
app = FastAPI()
client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


def stream_claude_response(question: str):
    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": question }
        ]
    ) as stream:
        for text in stream.text_stream:
            yield text


@app.post("/ask-stream")
def ask(request: AskRequest):
    # Note: try/except catches errors during generator creation only.
    # Errors mid-stream are not caught here — production hardening needed.
    try:
        message = stream_claude_response(request.question)
        return StreamingResponse(content=message, media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))