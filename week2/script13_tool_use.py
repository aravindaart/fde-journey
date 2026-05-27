import os
from datetime import datetime

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
    }
]

def get_current_time():
    return datetime.now().isoformat()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    answer: str = Field(..., min_length=1)
    input_tokens: int
    output_tokens: int
    stop_reason: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": request.message}],
            tools=tools
        )
        
        print(f"Turn 1 message: {message}")
        print(f"stop_reason: {message.stop_reason}")
        print(f"content: {message.content}")

        if message.stop_reason == "tool_use":
            tool_use_block = next(b for b in message.content if b.type == "tool_use")
            if tool_use_block.name == "get_current_time":
                tool_response = get_current_time()
                print(f"tool_use_block: {tool_use_block}")
                print(f"tool_name: {tool_use_block.name}")
                print(f"tool_response: {tool_response}")
            else:
                raise HTTPException(status_code=500, detail=f"Unknown tool: {tool_use_block.name}")
        
            # Turn 2
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                tools=tools,
                messages=[
                    {"role": "user", "content": request.message},
                    {"role": "assistant", "content": message.content},
                    {"role": "user", "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_block.id,
                            "content": tool_response
                        }
                    ]}
                ]
            )

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