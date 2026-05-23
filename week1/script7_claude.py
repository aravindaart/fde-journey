import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Say hello to Aravindhan who just made his first Claude API call." }
    ]
)

print(message.content[0].text)