# Learnings Log

## Week 1
- 2026-05-23: Python throws TypeError when concatenating string + int. JS silently coerces. Python's strictness = safer production code.
- 2026-05-23: Python list = JS array. Python dictionary = JS object.
- 2026-05-23: return gives value back to caller. print only shows on screen.
- 2026-05-23: .items() returns key-value pairs. tuple unpacking splits them into two variables in one step.
- 2026-05-23: JSON file handling - `with open()` auto-closes file after use.
- 2026-05-23: "r" = read mode. "w" = write. "a" = append.
- 2026-05-23: f-strings are cleaner than + concatenation. {variable:.2f} = 2 decimal places.
- 2026-05-23: Python f-string equivalent of JS toFixed() is :.2f inside {}.
- 2026-05-23: HTTP requests - response.text is raw string. response.json() converts it to a Python dictionary you can navigate.
- 2026-05-23: APIs often wrap single items in a list. Use [0] to get first item.
- 2026-05-23: load_dotenv() loads .env file into environment variables.
- 2026-05-23: Never hardcode API keys. os.getenv() reads from environment.
- 2026-05-23: LLM API responses wrap content in a list. [0] gets the text block.
- 2026-05-23: Use Haiku for dev/learning. Sonnet for production quality.
- 2026-05-23: input() pauses program and waits for user to type. Returns a string.
- 2026-05-23: \n in print() creates a blank line. Small but improves readability.
- 2026-05-23: LLMs don't have real-time data. They admit it and redirect. This is the honest behaviour we'll test with evals in Week 6.
- 2026-05-24: API field names should describe what the data is, not just that it exists. question/answer beats message/message. Future-you debugging at 2am will thank present-you.
- 2026-05-24: Be strict in what you accept. Reject contract violations loudly. Silent conversion hides bugs in the caller's code.
- 2026-05-24: Server-side validation is non-negotiable. Frontend validates for UX, backend validates for correctness. Never trust the client — not your own frontend, not anyone else's. Strict contracts catch bugs early. Lenient contracts hide them.
- 2026-05-24: Python type annotations (x: int) are normally just hints — not enforced at runtime. Pydantic turns them into actual runtime validation. That's the whole point of Pydantic.
- 2026-05-24: Field(...) — three dots (Ellipsis) means "required, no default." Any other value in that slot makes the field optional with that default. ... is a sentinel — a signal value, not real data.
- 2026-05-24: Pydantic validates both directions: request models protect the server from bad client input, response models protect clients from bugs in the server. Validation at both edges of the API.
- 2026-05-24: A Pydantic model has three useful forms — print(obj) for debugging, obj.field for accessing values, obj.model_dump() for converting to a dict. Know all three.
- 2026-05-24: Pydantic errors include type codes (missing, string_type, string_too_short) — these are machine-readable, not just human strings. FastAPI turns them into structured 422 responses automatically.
- 2026-05-24: Pydantic fails fast and loud with precise error messages — a typo'd field name is identified to the byte. This is what makes Python APIs debuggable. Without validation, the bug would surface 4 layers deep with no clue what went wrong.
- 2026-05-24: Pydantic v2 ≠ v1. v1 used class Config: for settings — different syntax. When googling Pydantic answers, check the version. Most tutorials older than 2024 are v1.
- 2026-05-24: Pydantic v2's validation engine is written in Rust (pydantic_core). That's why it's fast enough for production. Framework you use day-to-day, Rust engine you never touch.
- 2026-05-24: Python naming (PEP 8): packages = lowercase, classes = PascalCase, functions/variables = snake_case, constants = UPPER_SNAKE_CASE. Strictly enforced by convention — linters warn on violations.
- 2026-05-24: PEP 8 blank lines: 2 between top-level definitions (imports → code, function → function, class → class). 1 between methods inside a class or logical chunks inside a function. Linters enforce this.
- 2026-05-24: `ClassName()` calls the class constructor and returns an instance. `function_name()` calls a function and returns its return value. Capitalization (PEP 8) tells you which is which at a glance. Python has no `new` keyword — the parentheses do the work.
- 2026-05-24: `app = FastAPI()` creates ONE instance of the FastAPI class. `app` is that specific instance with its own routes and state. You could create multiple FastAPI instances in one process, but typically you create one per service.
- 2026-05-24: `@` syntax in Python is a decorator — a function that wraps another function to add behaviour. `@app.post("/ask")` registers the function below it as a route handler for POST /ask. Same concept as `@Post('/ask')` in NestJS or `@PostMapping` in Spring.
- 2026-05-24: FastAPI's `response_model=AskResponse` validates the return value against the Pydantic model before sending it back. Validation on both edges of the endpoint — request via function parameter type, response via `response_model`.
- 2026-05-24: FastAPI uses parameter type annotations as the contract. `def ask(request: AskRequest)` makes FastAPI automatically parse JSON body, validate against AskRequest, and pass the instance to your function. Zero plumbing code.
- 2026-05-24: `->` in Python is a return type annotation. `def foo() -> Bar` says "this function returns a Bar." Same concept as `: Bar` in TypeScript. In vanilla Python it's just a hint — for runtime enforcement in FastAPI, use `response_model=` in the decorator.
- 2026-05-24: In FastAPI you work in Pydantic instances end-to-end. Return an instance, not a dict — FastAPI handles serialization. Same pattern as `FastAPI()` constructing an app instance — `AskResponse(answer="...")` constructs a response instance.
- 2026-05-24: Function name ≠ URL path. They're independent. Decorator's first arg is the URL clients use; function name is for your codebase. Name the function after what it does, not after plumbing.
- 2026-05-24: Python reads top-to-bottom. A name must exist before it's referenced. Define things in dependency order: things being used go ABOVE things using them. JS has hoisting; Python doesn't.
- 2026-05-24: FastAPI auto-generates OpenAPI docs at `/docs` from Pydantic models and route decorators. Every field, type, constraint (min_length, max_length, required) appears in the public schema. Zero manual docs.
- 2026-05-24: Every FastAPI endpoint with a Pydantic body gets a 422 Validation Error response documented automatically. The error format (`detail`, `loc`, `msg`, `type`) is Pydantic's structured error output, now exposed as a contract clients can rely on.
- 2026-05-24: In FastAPI, Pydantic models are the SINGLE SOURCE OF TRUTH for the API contract: code, validation, docs, error schemas all derived from one place. No drift between code and docs — they can't disagree.
- 2026-05-24: HTTP 422 Unprocessable Entity = "request was parseable but failed validation rules." Distinct from 400 (malformed request) and 500 (server error). FastAPI returns 422 specifically for Pydantic validation failures.
- 2026-05-24: FastAPI 422 error body has shape `{"detail": [{"type", "loc", "msg", "input"}, ...]}`. `loc` is a path through the structure (["body", "field_name", ...]). `detail` is an array because one request can have multiple validation errors. Always iterate, don't just read `detail[0]`.
- 2026-05-24: Pydantic error `type` codes are machine-readable signals for clients to branch on: `missing` (field absent), `string_type` (wrong type), `string_too_short` / `string_too_long` (length violation). Build client UIs that switch on `type`, don't parse the `msg` string.
- 2026-05-24: Pydantic error `ctx` field carries the violated rule's parameters (e.g. `{"min_length": 1}`, `{"max_length": 1000}`). Lets clients render error messages dynamically — change the rule on the server, error messages update automatically.
- 2026-05-24: Pydantic does NOT silently coerce or fuzzy-match. A typo'd field is "missing" — full stop. Strict validation surfaces client bugs immediately instead of letting them fester.
- 2026-05-24: API design lifecycle distinction: module-level code runs ONCE at startup, function-body code runs PER REQUEST. Expensive, stateless objects (HTTP clients, DB connections, model loaders) belong at module level — create once, reuse for every request. Constructing them per-request is a classic performance bug.
- 2026-05-24: PEP 8 imports: 3 groups separated by blank lines — stdlib, third-party, local. Alphabetical within each group by module name. Mixing `import X` and `from X import Y` in a group is fine.
- 2026-05-24: PEP 8 spacing — assignments need spaces around `=` (`x = 1`). Keyword arguments in function calls do NOT (`func(x=1)`). Same symbol, different role, different spacing.
- 2026-05-24: Shipped script9 — FastAPI + Pydantic + Claude. First real AI API end to end. Request lifecycle: curl → uvicorn → FastAPI validation → Pydantic model → Claude SDK call → response object → AskResponse construction → JSON serialization → response back. This is the shape of every LLM service.
- 2026-05-24: Claude API responses include metadata your code throws away by default: `stop_reason` (why did Claude stop), `usage` (input/output tokens). `stop_reason="max_tokens"` means the response was TRUNCATED — silent data loss unless you surface it. Production APIs expose this to clients so they can detect cut-off responses.
- 2026-05-24: `max_tokens` is a hard ceiling, not a target. Setting `max_tokens=1024` and asking for a 2000-word essay = silent truncation, no error. Token ≈ 0.75 English words. 1024 tokens ≈ 750-800 words.
- 2026-05-24: Worst class of bug: returns wrong data without crashing, erroring, or logging. Truncated LLM output falls into this class. Defensive engineering = surfacing the metadata that lets you detect it.
- 2026-05-24: `git push` via remote name (`origin`) updates remote-tracking branches; pushing via full URL doesn't. Result: `git status` says "ahead by N commits" even after the push succeeded, because Git's local cache of origin is stale. Fix: `git fetch origin` refreshes it. Lesson: always `git push`, never `git push https://...`.
- 2026-05-24: POSIX convention: text files should end with a newline character. `\ No newline at end of file` in git diff = missing trailing newline. Fix by hitting Enter at file end. VS Code setting: "Files: Insert Final Newline" → true.
- 2026-05-24: Markdown consistency matters in docs — inline code (functions, identifiers, paths, keyword args) goes in backticks. Inconsistent formatting signals carelessness to anyone reading the repo. Match the style already established in the file.
- 2026-05-23: Week 1 complete. 9 scripts. FastAPI + Pydantic + Claude API end to end. Request lifecycle understood end to end. Ahead of schedule — Week 2 starts Monday.
- 2026-05-24: pip freeze dumps the entire environment. requirements.txt should only list direct imports — pip installs their sub-dependencies automatically.
- 2026-05-24: --host 0.0.0.0 binds to all network interfaces, required for cloud containers. Default 127.0.0.1 only accepts connections from the same machine — unreachable from outside.
- 2026-05-24: $PORT reads the port the cloud platform injects at runtime. Hardcoding a port number breaks deploys because the platform owns the port, not you.
- 2026-05-24: Render needs Root Directory and the exact Python filename in the start command. uvicorn script9_fastapi:app means find script9_fastapi.py and load the app object from it. Wrong filename = import error at runtime, not at build time.
- 2026-05-24: stop_reason lives on the message object directly, not inside message.usage. message.usage holds token counts only. Mixing them up is a runtime bug Pydantic will catch but the error message won't make it obvious.
- 2026-05-24: 503 Service Unavailable is the right status for upstream dependency failures. 422 is for validation failures, 500 is for unhandled crashes, 503 is for when your service can't reach something it depends on.
- 2026-05-24: Catching bare Exception and raising HTTPException converts raw Python stack traces into clean JSON error responses. Stack traces leaking to callers expose internals and signal amateur production code.
- 2026-05-24: Workflows use hardcoded sequences — the developer decides the flow. Agents use model-driven decision-making — the LLM decides what to do next. The distinction is who controls the flow, not how many steps there are.
- 2026-05-24: Augmented LLM = base LLM plus retrieval, tools, and memory. Workflows and agents are higher-level patterns built on top of this augmented base.
- 2026-05-24: Five workflow patterns: prompt chaining (sequential), parallelisation (concurrent), routing (conditional), orchestrator-subagent (delegate and consolidate), evaluator-optimiser (generate then critique in a loop).
- 2026-05-24: Default to the simplest solution. Single LLM call with retrieval is enough for most apps. Agents add latency and cost — only justified when the task needs model-driven decision-making that can't be hardcoded.

## Week 2
- 2026-05-25: The messages array is the memory. Stateless server plus client sends full history every request equals conversation with no database. This is how Anthropic and OpenAI APIs actually work.
- 2026-05-25: Literal["user", "assistant"] constrains a field to exact values. No Field() needed — the type does the full job. Only add Field() when you need length or range constraints.
- 2026-05-25: list[MessageBody] in a Pydantic model means a list of validated objects. The SDK expects dicts — convert with a list comprehension: [m.model_dump() for m in request.messages].
- 2026-05-25: System prompt belongs server-side always. Client sends messages only. Loading from env with a hardcoded fallback lets ops override without a code deploy.
- 2026-05-25: List comprehension syntax: [expression for item in iterable]. Transforms every item in one line.
- 2026-05-25: yield pauses a function and sends one value to the caller, then resumes from that line next time. A function with yield is a generator. return ends the function entirely.
- 2026-05-25: Calling a generator function does not run the function body. It returns a generator object. The body runs when something iterates the object — one yield at a time.
- 2026-05-25: client.messages.stream() needs a with block because it opens a network connection. with guarantees the connection closes even if an exception is thrown mid-stream.
- 2026-05-25: stream.text_stream is a generator that yields plain text chunks. It is not the same shape as a completed message response — no .content, no .usage, no .stop_reason.
- 2026-05-25: StreamingResponse wraps a generator. FastAPI pulls one chunk at a time and sends it to the client immediately. The client receives tokens as they arrive, not after the full response is ready.
- 2026-05-25: Streaming endpoints do not use response_model. response_model validates a complete object — streaming has no complete object to validate.
- 2026-05-25: The try/except on a streaming endpoint only catches errors during generator creation, not during iteration. The actual Claude API call happens when FastAPI iterates the generator — after the return statement. Errors mid-stream are a production hardening problem.
- 2026-05-27: Context window is the total token budget for one API call — system prompt plus all messages plus the response must fit inside it. It is not just conversation history.
- 2026-05-27: Sliding window is the simplest context management strategy — keep only the last N messages, drop the oldest. Drop in pairs (user + assistant) to preserve the strict alternating order Claude requires.
- 2026-05-27: Python slice messages[-n:] returns the last n items. If n exceeds the list length, Python returns the whole list — no error, no guard needed.
- 2026-05-27: input_tokens in the response is a direct measure of context size. Use it to verify trimming is working — send a long history and watch the token count stay bounded.
- 2026-05-27: tool_use is not agentic — it's a message type. The agent loop is what's agentic. Anthropic gives you the primitive; your code decides what to do with it.
- 2026-05-27: input_schema is required for zero-argument tools - I initially created tool without input_schema which ends in rejection from claude.
- 2026-05-27: role: "user" for tool_result, not role: "tool" — Anthropic has no tool role. OpenAI does. Different design choice, worth knowing
- 2026-05-27: Claude tool use is a TWO-TURN flow — first the model requests a tool (`stop_reason="tool_use"`), then the backend executes the real function and sends the result back in a second API call.
- 2026-05-27: `message.content` is a list of structured blocks (`text`, `tool_use`, etc.), not just plain text. Tool calls include metadata like `id`, `name`, and `input`.
- 2026-05-27: Tool execution is fully controlled by the backend. The LLM can REQUEST tools, but only your server can safely execute functions, APIs, databases, or external actions.
- 2026-05-27: Tool results must be sent back using a `tool_result` block with the original `tool_use_id`. Since the API is stateless, the second request must include the full conversation history.
- 2026-05-31: The loop is what makes it agentic. Script 13 was the primitive; the while loop turns it into an agent that drives its own multi-step process. Claude passes one tool's output as the next tool's input by itself — the loop enables data flow between tools that a hardcoded flow can't do.
- 2026-05-31: Before reusing a line from a previous script, check that the data shape matches. .model_dump() works on Pydantic models; plain dicts don't have it. Same trap as carrying compact_messages from script 12 into script 13. Pattern: when reusing code, ask "is the input here the same type as it was there?"
- 2026-05-31: JSON Schema properties defines which keyword arguments Claude can generate for a tool. required defines which arguments must always be present.
- 2026-05-31: func(**tool_input) unpacks a dictionary into keyword arguments. Example: {"minutes": 30} becomes func(minutes=30).
- 2026-05-31: A dispatch dictionary (tools_dict) is a scalable pattern for tool execution. It maps tool names to Python functions and avoids long if/elif chains.
- 2026-05-31: datetime.fromisoformat() converts an ISO datetime string into a Python datetime object. timedelta(minutes=30) adds time duration arithmetic cleanly.
- 2026-05-31: Multi-tool agent loops need an iteration cap to prevent infinite tool-calling loops. Exiting due to max iterations is a controlled failure case, not a successful completion.
- 2026-05-31: Iteration logging (iteration + stop_reason) is critical for debugging agent behaviour because tool workflows span multiple API calls and state transitions.

## Week 3

2026-05-31: OpenAI Chat Completions uses a messages array containing explicit roles (system, user, assistant) as the conversation contract.
2026-05-31: OpenAI responses are nested under choices[0].message.content, unlike Anthropic where text lives inside content[0].text.
2026-05-31: OpenAI token usage fields are named prompt_tokens and completion_tokens; Anthropic uses input_tokens and output_tokens.
2026-05-31: OpenAI uses finish_reason while Anthropic uses stop_reason. Same concept — why generation stopped — different naming conventions.
2026-05-31: SDKs from different providers solve the same problem with different response shapes. Production integrations depend heavily on reading provider docs carefully instead of assuming APIs are interchangeable.
2026-05-31: OpenAI nests finish_reason inside choices[0] because the API was designed to support n>1 — multiple completions per call, each with its own finish_reason. Anthropic returns one response per call so stop_reason sits at the top level.
- 2026-05-31: Different LLM providers can expose different SDKs and response shapes while sharing the same external API contract in your application.
- 2026-05-31: Normalisation is a core backend pattern — provider-specific responses are transformed into one consistent internal response model (AskResponse).
- 2026-05-31: Environment variables are useful for runtime feature switching. LLM_PROVIDER allows changing behaviour without modifying application code.
- 2026-05-31: Separating provider logic into call_llm() keeps route handlers thin and focused on HTTP responsibilities instead of business logic.
- 2026-05-31: OpenAI and Anthropic use different parameter conventions for system prompts:
OpenAI → system message inside messages[]
Anthropic → separate system= parameter
- 2026-05-31: ValueError is appropriate for invalid internal configuration states like unsupported provider names because the failure comes from server configuration, not client input.
- 2026-05-31: Same prompt, same system prompt, different providers produce different response styles and token counts. Claude returned formatted markdown with 154 output tokens; OpenAI returned a single sentence with 15. Model personality and verbosity vary across providers — this is why evals matter, correctness alone isn't enough to measure.
- 2026-05-31: Embeddings convert text into high-dimensional numeric vectors representing semantic meaning.
- 2026-05-31: Semantic similarity search compares meaning rather than exact words. Similar concepts can match even when phrased differently.
- 2026-05-31: Cosine similarity measures the angle between two vectors. Values closer to 1 mean higher similarity.
- 2026-05-31: np.dot(a, b) calculates the dot product between vectors, while np.linalg.norm() calculates vector magnitude.
- 2026-05-31: Cosine similarity formula: `np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))`
dot_product / (magnitude_a * magnitude_b)
- 2026-05-31: OpenAI embeddings API returns embeddings in the same order as the input list. embeddings[0] corresponds to the query because the query was the first input.
- 2026-05-31: zip(menu, menu_embeddings) iterates two lists together in parallel — pairing each menu item with its corresponding embedding.
- 2026-05-31: Sorting tuples works lexicographically in Python. (similarity, item) sorts by similarity first because it's the tuple's first value.
- 2026-05-31: NumPy functions like np.dot() and np.linalg.norm() accept plain Python lists because NumPy automatically converts them internally. For small learning scripts this is fine, but explicit np.array() conversion is clearer and safer in production code.
2026-05-31: This script is the retrieval core of RAG. In production, pre-compute embeddings for all documents and store them. At query time, embed the question, find the most similar chunks, and send only those to the LLM — not the entire document set.
- 2026-05-31: A vector database stores embeddings and performs semantic similarity search efficiently without manually computing cosine similarity in application code.
- 2026-05-31: ChromaDB collections are similar to database tables — they group related documents, embeddings, metadata, and IDs together.
- 2026-05-31: `collection.add()` stores:
  * `documents` → raw text
  * `metadatas` → structured metadata
  * `ids` → unique document identifiers
- 2026-05-31: ChromaDB automatically generates embeddings internally when using `query_texts`, removing the need for explicit embedding API calls in simple use cases.
- 2026-05-31: `n_results=1` limits the similarity search to the single closest matching document.
- 2026-05-31: ChromaDB matches semantically similar text, not exact keywords. `"I want a mango drink"` can retrieve `"Mango milk tea with tapioca pearls"`.
- 2026-05-31: ChromaDB document IDs must be unique within a collection. Reusing the same ID updates/replaces existing entries instead of creating duplicates.
- 2026-05-31: `chromadb.Client()` creates an in-memory database. Data disappears when the script exits because nothing is persisted to disk.
- 2026-05-31: For persistent storage, use `chromadb.PersistentClient(path="./chroma_db")` so collections survive application restarts.
- 2026-05-31: Running ingestion repeatedly with the same IDs behaves like an upsert rather than creating duplicate documents. In production, using `collection.upsert()` explicitly makes this intent clearer.
- 2026-05-31: Embedding models must be consistent across ingestion and query. Vectors from different models (e.g. OpenAI text-embedding-3-small vs ChromaDB's all-MiniLM-L6-v2) live in different vector spaces — comparing them produces meaningless similarity scores.
- 2026-05-31: RAG (Retrieval-Augmented Generation) combines retrieval systems with LLM generation. Retrieval fetches relevant context first; the LLM answers using that context.
- 2026-05-31: Embedding ingestion is usually a startup-time operation, not a per-request operation. Static datasets should be embedded once and reused.
- 2026-05-31: `PersistentClient(path="./chroma_db")` stores vector data on disk so embeddings survive application restarts.
- 2026-05-31: `collection.count()` can be used as a simple ingestion guard to avoid re-embedding the same dataset every startup.
- 2026-05-31: In RAG pipelines, retrieval and generation are separate stages:
  1. Generate embedding for the query
  2. Retrieve semantically similar documents
  3. Inject retrieved context into the LLM prompt
  4. Generate the final answer
- 2026-05-31: `query_embeddings=[...]` allows querying ChromaDB using precomputed embeddings instead of raw text.
- 2026-05-31: Retrieval commonly returns multiple chunks (`n_results=3`) because one document may not contain enough context to answer fully.
- 2026-05-31: Retrieved documents are often concatenated into one context block before sending to the LLM.
- 2026-05-31: Prompt augmentation is the core idea of RAG — dynamically injecting retrieved external knowledge into the user prompt.
- 2026-05-31: RAG reduces hallucination risk because the model answers from retrieved context instead of relying purely on parametric memory.
- 2026-05-31: Even with RAG, the model can still hallucinate or ignore context. Explicit grounding instructions improve reliability but are not perfect guarantees.
- 2026-05-31: Production RAG systems typically separate:
  * ingestion pipeline
  * vector database
  * retrieval layer
  * generation layer
- 2026-05-31: This script uses OpenAI embeddings for retrieval and OpenAI chat completions for generation, but the retrieval layer and generation layer can use different providers independently.
- 2026-05-31: ChromaDB query results nest documents as a list of lists. 
  Outer list = one entry per query (supports batched queries). 
  Inner list = retrieved documents for that query. 
  Single query pattern: results["documents"][0] gets your result set.

## Week 4

- 2026-06-01: Chunking splits large documents into smaller pieces before embedding and retrieval.
- 2026-06-01: Fixed-size chunking is simple but can silently break semantic meaning when related information lands in different chunks.
- 2026-06-01: Overlapping chunking repeats part of the previous chunk in the next chunk so important context survives chunk boundaries.
- 2026-06-01: Overlap improves retrieval reliability because at least one chunk is likely to contain the full context needed to answer a query.
- 2026-06-01: Character-based chunking can split words mid-token (`"pista"` / `"chio"`). Production systems usually chunk on word, sentence, or paragraph boundaries instead.
- 2026-06-01: Python slicing `text[i:i+chunk_size]` safely handles end-of-string boundaries without manual checks.
- 2026-06-01: `start += chunk_size - overlap` moves the sliding window forward while preserving shared context between adjacent chunks.
- 2026-06-01: RAG systems have two separate failure modes:
  1. retrieval failure → the correct information was never retrieved
  2. grounding failure → the LLM ignored or invented beyond retrieved context
- 2026-06-01: Better prompting can reduce hallucinations but cannot recover information missing from retrieval.
- 2026-06-01: Retrieval gaps often happen when important sentences are split across chunk boundaries and the relevant chunk is not included in the top-k retrieval results.
- 2026-06-01: Increasing `n_results` can improve recall because more neighbouring chunks are passed into the final prompt.
- 2026-06-01: Larger chunk sizes reduce the risk of splitting related information but also increase irrelevant context and token usage.
- 2026-06-01: Multi-part user questions are especially difficult for naive RAG because different parts of the answer may exist in different chunks.
- 2026-06-01: Semantic retrieval optimises for similarity, not factual completeness. The retrieved chunk may discuss the topic while still missing the exact answer detail.
- 2026-06-01: Strong grounding prompts like `"Answer strictly from context"` improve honesty but are not perfect guarantees against hallucination.
- 2026-06-01: Retrieval quality directly limits generation quality. The LLM cannot reason over information it never received.
- 2026-06-01: Honest failure is better than fabricated answers in production RAG systems. A system saying `"I don't have that information"` is safer than confident hallucination.
- 2026-06-01: Metadata filtering constrains vector search to a subset of documents, improving retrieval precision.
- 2026-06-01: ChromaDB supports metadata filters using `where={}` during queries.
- 2026-06-01: Semantic similarity alone is insufficient for accurate retrieval because related concepts from the wrong document category can contaminate results.
- 2026-06-01: Retrieval quality improves when embeddings are combined with structured metadata constraints instead of relying only on vector similarity.
- 2026-06-01: Document tagging is an important RAG design pattern. Separating content into categories like `menu`, `policy`, and `operations` helps retrieval stay contextually relevant.
- 2026-06-01: Filtering reduces the retrieval search space, which becomes increasingly important as the number of chunks grows.
- 2026-06-01: `collection.query(where={"type": doc_type})` performs hybrid retrieval — semantic search constrained by structured metadata.
- 2026-06-01: Cross-contamination happens when semantically similar chunks from unrelated sections appear in retrieval results.
- 2026-06-01: Proper metadata tagging can fix retrieval failures without changing embeddings, chunking strategy, or prompts.
- 2026-06-01: `zip(*chunks_with_meta)` is a Python unpacking pattern that separates tuples like `(chunk, metadata)` into two independent lists.
- 2026-06-01: Tool description quality directly affects tool routing accuracy. Vague tool descriptions increase the chance of incorrect tool selection.
- 2026-06-01: `tool_result` content must be a string. Lists or structured objects should be normalised before returning results to Claude.
- 2026-06-01: Claude can generate semantically improved retrieval queries instead of simply copying the user's original wording.
- 2026-06-01: Metadata-filtered retrieval improves routing quality by constraining semantic search to the correct document category.
- 2026-06-01: Chunking artifacts appear in real RAG answers when chunks split mid-sentence or mid-word, even if retrieval and routing are otherwise correct.
- 2026-06-01: Agent systems can combine operational tools and retrieval tools inside the same workflow, allowing one assistant to handle both actions and knowledge lookup.
- 2026-06-01: Retrieval quality problems become more visible in full pipelines because incomplete chunks directly degrade final generated answers.
- 2026-06-01: Tool routing and retrieval are separate concerns — correct tool selection does not guarantee correct retrieval quality.
- 2026-06-01: `message.content[0].text` is safe in an agent loop that only exits when `stop_reason == "end_turn"`. The failure case is exiting the loop before verifying stop reason — Claude's last message could be a `tool_use` block with no `.text`.
- 2026-06-08: Evals measure three independent dimensions in a RAG+routing system: (1) retrieval accuracy — did the right chunk come back, (2) grounding accuracy — did the LLM answer from context not memory, (3) routing accuracy — did the right tool get selected. Missing any one gives an incomplete picture.
- 2026-06-08: An eval test set needs expected answers. Two sources: golden answers written manually for known queries, or LLM-generated answers reviewed and approved. The second is faster but needs human review before trusting.
- 2026-06-08: LLM-as-Judge scoring: ask a second LLM call to rate the answer on relevance, groundedness, and completeness (1–5 each). This is the production pattern — not string matching against expected answers.

## Week 4 summary
Scripts 20–23 complete. Chunking, top-k retrieval, metadata filtering, RAG + tool routing. Two RAG failure modes named and understood. Third dimension (routing eval) introduced. Dual-provider pattern confirmed. Week 4 closed. Script 24 (eval harness) is Week 5 task 1.

- 2026-06-20: The 2026-06-08 entries above describe planned LLM-as-judge scoring. The eval harness actually built and committed today (script24) uses keyword-based scoring across routing/retrieval/grounding instead — a simpler first pass. LLM-as-judge scoring is a separate follow-up, not yet built.
- 2026-06-20: assert stops execution on first failure — wrong tool for an eval harness, which must run every test case and report results even when some fail. Boolean scoring (pass/fail flags + counters) replaces assert for eval loops.
- 2026-06-20: Real script24 run surfaced four findings: chunk_size=200 too aggressive for named-entity retrieval (a specific drink name like "Galactic Pistachio" got split or buried, retrieval missed it); one case showed a routing stall where Claude asked for missing input (customer ID) instead of calling any tool; one test case ("How many points do I have?" with no customer ID) was a flawed test design, not a system failure; the order-status case passed cleanly end to end.
- 2026-06-20: A test case must be answerable from the data and tools available, with no missing required inputs. An ambiguous test case produces an indeterminate eval result that looks like a system failure but is actually a test design failure.

## Week 5

- 2026-06-20: LLM-as-judge is not deterministic. Running the same test case twice (Fossil Praline Crunch Shake redemption) produced different grounded verdicts across runs — one run accepted "asks for missing info" as grounded, another flagged the same behavior as fabricating capability it didn't have. Judge variance is a real production concern: keyword eval is deterministic but blind to nuance; LLM-as-judge is nuanced but inconsistent across runs. Neither is sufficient alone.
- 2026-06-20: Judge groundedness only applies to RAG-sourced answers. Tool-based answers (order status, loyalty points) can't be judged against retrieved_chunks since that list stays empty for non-RAG tools — and passing raw tool output (potential customer PII) to a third-party judge LLM is a real compliance risk, not just a design preference. Decision: skip grounded scoring for tool-only cases, track eligibility separately (grounded_eligible), and only judge relevance for those cases.
- 2026-06-20: A metric that can be forced to a fixed value by construction (e.g. grounded defaulting to true with no real evaluation) inflates pass rates without measuring anything. Eval denominators must match what was actually evaluated, not the full test set size — grounded_passes/grounded_eligible, not grounded_passes/len(test_cases).
- 2026-06-22: Langfuse decorators operate at function-call boundaries, not internal control-flow boundaries. Decorating call_llm() with @observe(as_type="generation") could only ever create a single generation span because call_llm() itself is invoked once, even though it may execute multiple Claude API calls inside its while loop. To get one generation span per model invocation, the generation decorator must be placed on call_claude(), the function that actually wraps the Anthropic API call.
- 2026-06-22: Observability data has the same privacy considerations as application logs. Tool inputs and outputs may contain customer IDs, order IDs, loyalty balances, or other user-specific information. Decision: disable automatic tool payload capture using capture_input=False and capture_output=False, then record only operational metadata (e.g. lookup_completed=True/False) through update_current_span().
- 2026-06-22: Metadata should describe execution state, not replicate business data. An early implementation stored the actual loyalty points value (e.g. metadata={"loyalty_points": points}) — moving sensitive data from output to metadata rather than redacting it. Recording success/failure signals (lookup_completed=True/False) proved more useful and removed the privacy risk entirely.
- 2026-06-22: Span updates should occur after the observed event has actually completed. Recording lookup_completed=True before generating the tool result creates traces that can report success even when the operation later fails. The final implementation computes the result first, then records success metadata, and records failure metadata inside the exception path.
- 2026-06-22: Observability instrumentation should preserve existing error semantics. Early iterations accidentally swallowed exceptions or used invalid exception handling patterns, which made traces appear successful when failures occurred. Decision: record failure metadata and re-raise the original exception so monitoring data and application behavior remain consistent.
- 2026-06-22: Langfuse installation exposed environment compatibility issues that were unrelated to the agent itself. Dependency conflicts between Python versions, virtual environments, and package requirements consumed more implementation time than the actual instrumentation work. Observability libraries should be validated against the project's runtime environment before beginning integration.