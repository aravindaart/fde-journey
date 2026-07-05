# script27_langgraph.py
import os
from typing import TypedDict
from random import randint
from chromadb import PersistentClient
from dotenv import load_dotenv
from anthropic import Anthropic

from openai import OpenAI
from langgraph.graph import StateGraph, START, END

load_dotenv()
chroma_client = PersistentClient(path="./chroma_db")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
text = open("data/bubble_tea.txt").read()
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant for a bubble tea shop. Answer questions based on the provided context and use the tools when necessary.")

collection = chroma_client.get_or_create_collection("bubble_tea")

metadata = {
    "SIGNATURE DRINKS": "menu",
    "PREMIUM CREATIONS": "menu",
    "SNACKS": "menu",
    "LOYALTY AND MEMBERSHIP": "policy",
    "ORDERING AND OPERATIONS": "operations",
}


# ── State ────────────────────────────────────────────────────────────────
class AgentState(TypedDict):
    messages: list[dict]
    iteration: int
    stop_reason: str

# ── Tools (copy from script26 — same definitions, nothing changes) ───────
tools_list = [
    {
        "name": "search_knowledge_base",
        "description": "Search the knowledge base for information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "doc_type": {
                    "type": "string",
                    "description": "The type of document to search for available values are 'menu', 'policy', and 'operations'"
                }
            },
            "required": ["query", "doc_type"]
        }
    },
    {
        "name": "get_loyalty_points",
        "description": "Get the loyalty points for a customer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The ID of the customer"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "get_order_status",
        "description": "Get the status of an order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The ID of the order"
                }
            },
            "required": ["order_id"]
        }
    }
]

order_status_list = ["In Progress", "Completed", "Cancelled", "Delayed"]

sections = list(filter(lambda s: s.strip(), text.split("---")))


def ingest_with_metadata(text: str, doc_type: str, chunk_size: int, overlap: int):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append((chunk, {"type": doc_type}))
        start += chunk_size - overlap
    return chunks


def ingest_sections(sections: list[str]):
    sections_by_type = {}
    for section in sections:
        section_name = section.split("\n\n")[1].strip()
        doc_type = metadata.get(section_name, "operations")
        if doc_type not in sections_by_type:
            sections_by_type[doc_type] = []
        sections_by_type[doc_type].append(section)

    for doc_type, doc_sections in sections_by_type.items():
        text_block = "\n\n".join(doc_sections)
        chunks_with_meta = ingest_with_metadata(text_block, doc_type, chunk_size=200, overlap=50)
        chunks, metadatas = map(list, zip(*chunks_with_meta))
        embeddings = openai_client.embeddings.create(input=chunks, model="text-embedding-3-small").data
        collection.add(
            documents=chunks,
            embeddings=[e.embedding for e in embeddings],
            metadatas=metadatas,
            ids=[f"{doc_type}_chunk_{i}" for i in range(len(chunks))]
        )


if collection.count() == 0:
    ingest_sections(sections)


def retrieve_filtered(query_embedding: list[float], doc_type: str, n_results: int) -> list[str]:
    results = collection.query(query_embeddings=[query_embedding], where={"type": doc_type}, n_results=n_results)
    return results["documents"][0]


def search_knowledge_base(query: str, doc_type: str) -> str:
    query_embedding = openai_client.embeddings.create(input=[query], model="text-embedding-3-small").data[0].embedding
    return "\n".join(retrieve_filtered(query_embedding, doc_type, 3))


def get_loyalty_points(customer_id: str) -> int:
    try:
        points = randint(0, 1000)
        return points
    except Exception as e:

        raise e



def get_order_status(order_id: str) -> str:
    try:
        status = order_status_list[randint(0, len(order_status_list) - 1)]
        return status
    except Exception as e:
        raise e
    
tools_dict = {
    "search_knowledge_base": search_knowledge_base,
    "get_loyalty_points": get_loyalty_points,
    "get_order_status": get_order_status
}

# ── Nodes ────────────────────────────────────────────────────────────────
def call_llm(state: AgentState) -> dict:
    
    # TODO: call Claude with state["messages"]
    message =  anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=state["messages"],
        tools=tools_list
    )
    # TODO: append assistant message to messages
    assistant_message = {
        "role": "assistant",
        "content": [block.model_dump() for block in message.content],
    }
    # TODO: return updated messages and stop_reason
    return {
        "messages": state["messages"] + [assistant_message],
        "stop_reason": message.stop_reason,
    }

def execute_tools(state: AgentState) -> dict:
    last_message = state["messages"][-1]
    # TODO: find the tool_use block in the last assistant message
    tool_use = next(
        block
        for block in last_message["content"]
        if block["type"] == "tool_use" 
    )
    
    # TODO: execute the tool
    tool_fn = tools_dict.get(tool_use["name"])
    if tool_fn is None:
        raise ValueError(f"Unknown tool: {tool_use.name}")
    result = tool_fn(**tool_use["input"])

    # TODO: build tool_result block
    tool_result_message = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use["id"],
                "content": str(result),
            }
        ],
    }
    # TODO: append tool_result message to messages
    # TODO: return updated messages and incremented iteration
    return {
        "messages": state["messages"] + [tool_result_message],
        "iteration": state["iteration"] + 1,
    }

# ── Routing ──────────────────────────────────────────────────────────────
def route(state: AgentState) -> str:
    # TODO: if stop_reason == "tool_use" AND iteration < max_iterations, return "tools"
    if state["stop_reason"] == "tool_use" and state["iteration"] < MAX_ITERATIONS:
        return "execute_tools"
    # TODO: otherwise return END
    return END

# ── Graph ────────────────────────────────────────────────────────────────
MAX_ITERATIONS = 10

builder = StateGraph(AgentState)
builder.add_node("call_llm", call_llm)
builder.add_node("execute_tools", execute_tools)
builder.add_edge(START, "call_llm")
builder.add_conditional_edges("call_llm", route)
builder.add_edge("execute_tools", "call_llm")
graph = builder.compile()

# ── Entry point ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    query = input("You: ")
    initial_state = {
        "messages": [{"role": "user", "content": query}],
        "iteration": 0,
        "stop_reason": ""
    }
    result = graph.invoke(initial_state)
    print(f"Assistant: {result['messages'][-1]['content'][0]['text']}")