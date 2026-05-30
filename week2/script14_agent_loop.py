import os
from datetime import datetime, timedelta

from typing import Literal
from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


load_dotenv()
app = FastAPI()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tools = [
    {
        "name": "get_current_time",
        "description": "Get the current time in ISO format.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "add_minutes",
        "description": "Add minutes to an ISO datetime string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "datetime_string": {
                    "type": "string",
                    "description": "ISO datetime string"
                },
                "minutes": {
                    "type": "integer",
                    "description": "Number of minutes to add"
                }
            },
            "required": ["datetime_string", "minutes"]
        }
    }
]

def get_current_time():
    return datetime.now().isoformat()

def add_minutes(datetime_string: str, minutes: int):
    dt = datetime.fromisoformat(datetime_string)
    new_dt = dt + timedelta(minutes=minutes)
    return new_dt.isoformat()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    answer: str = Field(..., min_length=1)
    input_tokens: int
    output_tokens: int
    stop_reason: str

tools_dict = {
    "get_current_time": get_current_time,
    "add_minutes": add_minutes
}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    messages = [{"role": "user", "content": request.message}]
    iteration = 0
    max_iterations = 10
    finished = False

    try:
        while iteration < max_iterations:
            
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                messages=messages,
                tools=tools
            )
            messages.append({"role": "assistant", "content": message.content})

            if message.stop_reason != "tool_use":
                finished = True
                break
            
            tool_results = []
            for block in message.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    if tool_name in tools_dict:
                        result = tools_dict[tool_name](**tool_input)
                    else:
                        raise HTTPException(status_code=500, detail=f"Unknown tool: {tool_name}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})

            iteration += 1

        if not finished:
            raise HTTPException(status_code=503, detail="Max iterations reached")
        return ChatResponse(
            answer=message.content[0].text,
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
            stop_reason=message.stop_reason
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    