import os

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic


load_dotenv()
app = FastAPI()
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client_anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class AskResponse(BaseModel):
    answer: str = Field(..., min_length=1)
    input_tokens: int
    output_tokens: int
    stop_reason: str


def call_llm(question: str) -> AskResponse: 
    if LLM_PROVIDER == "anthropic":
        message = client_anthropic.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": question }
            ]
        )
        return AskResponse(answer=message.content[0].text, input_tokens=message.usage.input_tokens, output_tokens=message.usage.output_tokens, stop_reason=message.stop_reason)
    elif LLM_PROVIDER == "openai":
        message = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question }
            ]
        )
        return AskResponse(answer=message.choices[0].message.content, input_tokens=message.usage.prompt_tokens, output_tokens=message.usage.completion_tokens, stop_reason=message.choices[0].finish_reason)
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        response = call_llm(request.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))