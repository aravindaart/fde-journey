import os
from random import randint

from chromadb import PersistentClient
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

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

tools = [
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

verdict_tools = [
    {
        "name": "submit_verdict",
        "description": "Submit a grading verdict for an LLM-generated answer, evaluating whether it is grounded in the provided context and relevant to the user's question.",
        "input_schema": {
            "type": "object",
            "properties": {
                "grounded": {
                    "type": "boolean",
                    "description": "True if the answer only uses information present in the retrieved context, with no invented or hallucinated facts. False if any part of the answer goes beyond what the context supports."
                },
                "relevant": {
                    "type": "boolean",
                    "description": "True if the answer directly addresses what the user asked. False if the answer is grounded but answers a different question than the one asked, or fails to address the user's actual query."
                },
                "reason": {
                    "type": "string",
                    "description": "A one-sentence explanation for the verdict, citing what in the answer or context led to the grounded/relevant decision."
                }
            },
            "required": ["grounded", "relevant", "reason"]
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
    return randint(0, 1000)


def get_order_status(order_id: str) -> str:
    return order_status_list[randint(0, len(order_status_list) - 1)]


tools_dict = {
    "search_knowledge_base": search_knowledge_base,
    "get_loyalty_points": get_loyalty_points,
    "get_order_status": get_order_status
}

def run_eval_agent(question: str) -> dict:
    messages = [{"role": "user", "content": question}]
    iteration = 0
    max_iterations = 10
    finished = False
    tools_called = []
    retrieved_chunks = []
    try:
        while iteration < max_iterations:
            message = anthropic_client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
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
                    tools_called.append(tool_name)
                    if tool_name in tools_dict:
                        result = tools_dict[tool_name](**tool_input)
                        retrieved_chunks.append(result) if tool_name == "search_knowledge_base" else None
                        print(f"Tool: {tool_name}, Input: {tool_input}, Result: {result}")
                    else:
                        raise Exception(f"Unknown tool: {tool_name}")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })

            messages.append({"role": "user", "content": tool_results})

            iteration += 1

        if not finished:
            raise Exception("Max iterations reached")
        print(f"Tools called: {tools_called}")
        print(f"Retrieved chunks: {retrieved_chunks}")
        print(f"Final answer: {message.content[0].text}")
        return {"answer": message.content[0].text, "tools_called": tools_called, "retrieved_chunks": retrieved_chunks}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"answer": "", "tools_called": tools_called, "retrieved_chunks": retrieved_chunks}


def judge_answer(question: str, context: str, answer: str, tools_called: list) -> dict:
    judge_prompt = f"""
    Question: {question}
    Retrieved context: {context}
    Answer to evaluate: {answer}
    Tools called during answer generation: {', '.join(tools_called) if tools_called else 'None'}
    """
    message = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="You are an impartial judge evaluating the quality of an LLM-generated answer based on the question asked and the retrieved context. "
       "If search_knowledge_base was not called, do not evaluate groundedness against retrieved context — instead, set grounded to true by default and base your reason only on relevance,"
       "If the retrieved context is empty, the answer can only be grounded if it explicitly asks for missing required information instead of fabricating an answer, or if it correctly states that no information is available — fabricating any specific fact with no context is never grounded. "
       "Provide a one-sentence explanation for your verdict.",
        messages=[{"role": "user", "content": judge_prompt}],
        tool_choice={"type": "tool", "name": "submit_verdict"},
        tools=verdict_tools
    )
    verdict_block = next((block for block in message.content if block.type == "tool_use" and block.name == "submit_verdict"), None)
    if verdict_block:
        return verdict_block.input
    else:
        raise Exception("No verdict submitted by the judge.")


test_cases = [
    {"question": "What time does Bubble Tea Lab close on Saturday?"},
    {"question": "Does the Galactic Pistachio drink contain nuts?"},
    {"question": "Can I redeem points for the Fossil Praline Crunch Shake?"},
    {"question": "How many points do I have?"},
    {"question": "What is the status of order BT123?"}
]

grounded_passes = 0
grounded_eligible = 0
relevant_passes = 0

for case in test_cases:
    print(f"\nQuestion: {case['question']}")
    result = run_eval_agent(case["question"])
    judge_result = judge_answer(case["question"], "\n".join(result["retrieved_chunks"]), result["answer"], result["tools_called"])
    print(f"Judge Verdict: {judge_result}")
    grounded_pass = judge_result["grounded"]
    relevant_pass = judge_result["relevant"]
    print(f"Grounded Pass: {grounded_pass}, Relevant Pass: {relevant_pass}, Grounded Eligible: {grounded_eligible}")    
    
    if result["tools_called"] and "search_knowledge_base" in result["tools_called"]:
        grounded_eligible += 1
        if grounded_pass:
            grounded_passes += 1
    if relevant_pass:
        relevant_passes += 1

print(f"\nSummary:")
print(f"Grounded Passes: {grounded_passes}/{grounded_eligible}")
print(f"Relevant Passes: {relevant_passes}/{len(test_cases)}")
print(f"Grounded Eligible: {grounded_eligible}/{len(test_cases)}")