# Week 6 - Docker (containerize script27) + FLAGSHIP_SPEC.md

### Dockerizing `script27_langgraph.py`

Packages the existing `script27_langgraph.py` LangGraph application into a Docker container. The application logic is unchanged from Week 5; this week focuses on creating a portable and reproducible runtime using Docker.

**Key question:** Why containerize the application?
**Answer:** Docker packages the application and its dependencies into a portable image that runs consistently across different environments.

**Key question:** Why use `python:3.12-slim`?
**Answer:** It provides a lightweight Python runtime with good compatibility for the project's dependencies. A clean build confirmed that no additional system packages were required.

---

## How to build

```bash
docker build -t week6-langgraph-agent:v1 .
```

## How to run

From the `week6/` directory:

```bash
docker run -it \
  --env-file ../.env \
  week6-langgraph-agent:v1
```

## Expected behaviour

* Docker builds the image successfully.
* The container prompts for a user query.
* The existing LangGraph workflow executes.
* The assistant prints the final response before the container exits.

## Engineering findings

**Base image:** `python:3.12-slim` was sufficient for this project. The image built successfully and the application ran without installing additional system packages.

**Layer caching:** Copying `requirements.txt` before the application source allows Docker to reuse the dependency layer when only source files change, reducing rebuild time.

**Environment variables:** API keys are supplied at runtime using `--env-file` instead of being stored inside the Docker image.

**Application data:** The knowledge base file is stored in `week6/data/` and becomes part of the Docker build context. The `COPY . .` instruction copies it into the image at build time, making the container self-contained without requiring bind mounts. This approach is suitable for deployments such as Cloud Run and Render, where host volume mounts are typically unavailable.

**Interactive execution:** Since the script uses `input()`, the container must be run with `-it` so Python can read user input from the terminal.

**Multiple tool calls:** Claude can emit multiple `tool_use` blocks for a single assistant response when answering compound queries. The tool execution logic collects all `tool_use` blocks, executes each requested tool, and returns one `tool_result` block per tool call inside a single user message, satisfying Anthropic's tool-use protocol.

**Build context:** `.dockerignore` excludes unnecessary files from the build context, keeping the image smaller and preventing unwanted files from being copied into the image.

## CLI → FastAPI Conversion

### Why was this changed?

The original application was designed as a command-line program that waited for user input using `input()`. This works well for local development but cannot be deployed as a Render Web Service because Render expects the application to start an HTTP server and listen on the port provided through the `PORT` environment variable.

To make the application deployable, the interactive CLI interface was replaced with a FastAPI endpoint while keeping the LangGraph workflow unchanged.

### What changed?

* Replaced terminal input (`input()`) with a FastAPI `POST /ask` endpoint.
* Added `AskRequest` and `AskResponse` Pydantic models for request validation and response serialization.
* Moved the `graph.invoke(initial_state)` call into the route handler.
* Kept the existing LangGraph workflow, nodes, edges, and state unchanged. Only the method of receiving user input changed.
* Updated the Docker runtime to start a Uvicorn server instead of executing the Python script directly.

### How to run

Build the Docker image:

```bash
docker build -t week6-langgraph-agent:v1 .
```

Run the container:

```bash
docker run \
  --env-file ../.env \
  -e PORT=8000 \
  -p 8000:8000 \
  week6-langgraph-agent:v1
```

The API will be available at:

```
http://localhost:8000
```

### Test the API

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are your signature drinks?"
  }'
```

Expected response:

```json
{
  "answer": "..."
}
```
