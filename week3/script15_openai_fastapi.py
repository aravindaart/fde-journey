import os

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class AskResponse(BaseModel):
    answer: str = Field(..., min_length=1)
    input_tokens: int
    output_tokens: int
    stop_reason: str


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        message = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.question }
            ]
        )
        print(message)
        return AskResponse(answer=message.choices[0].message.content, input_tokens=message.usage.prompt_tokens, output_tokens=message.usage.completion_tokens, stop_reason=message.choices[0].finish_reason)
    except OpenAIError as e:
        raise HTTPException(status_code=503, detail=str(e))