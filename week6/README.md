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
