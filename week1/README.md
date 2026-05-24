# Week 1 — Python Foundations

## Scripts

### script1_variables.py
Variables and type conversion.
**Key question:** Why do we need `str()` when concatenating an integer with a string?
**Answer:** Python is strict about types unlike JavaScript. Adding string + int 
throws a TypeError. `str()` explicitly converts the integer to a string first.

### script2_list.py
Lists and for loops.
**Key question:** What does `for skill in skills:` mean in plain English?
**Answer:** For each item in the list, temporarily call it `skill` and run 
the indented block with it. Python gives you the value directly, not the index.

### script3_function.py
Functions and return values.
**Key question:** What is the difference between `return` and `print`?
**Answer:** `print` shows something on screen but gives nothing back to your 
code. `return` gives a value back to the caller so it can be stored and reused.
If a function uses `print` instead of `return`, the caller gets `None`.

### script4_dictionary.py
Dictionaries and tuple unpacking.
**Key question:** What does `.items()` do and why two variables in the for loop?
**Answer:** `.items()` returns each entry as a key-value pair. Writing 
`for key, value in` automatically unpacks that pair into two variables — 
this is called tuple unpacking. We need `str(value)` because `years_experience` 
is an integer and Python won't concatenate string + int without conversion.

### script5_json.py
JSON file handling and f-strings.
**Key question:** What does `with open("file.json", "r") as file:` do?
**Answer:** Opens the file in read-only mode and automatically closes it when 
the indented block finishes — even if the code crashes. Without `with` you'd 
have to manually call `file.close()`.

**Key question:** What is an f-string?
**Answer:** A Python string prefixed with `f` that lets you embed variables 
directly inside `{}`. Cleaner than concatenation with `+`. 
`f"${price:.2f}"` is Python's equivalent of JS `toFixed(2)`.

### script6_http.py
HTTP requests and API responses.
**Key question:** What is `response.json()` doing?
**Answer:** The API returns raw text over HTTP. `response.json()` parses that 
raw string into a Python dictionary so your code can navigate it with keys 
like `data["current_condition"]`. Without it you just have a string.

**Key question:** Why `data["current_condition"][0]`?
**Answer:** APIs often wrap single items inside a list. `[0]` gets the first 
item from that list — which is the dictionary containing the actual weather data.

### script7_claude.py
First Claude API call using the Anthropic SDK.
**Key question:** What does `load_dotenv()` do?
**Answer:** Reads the `.env` file and loads its values into environment 
variables so your code can access them via `os.getenv()`.

**Key question:** Why not hardcode the API key directly in the script?
**Answer:** Hardcoded keys get committed to Git and become public. Anyone 
can find them and use your credits. Environment variables keep secrets out 
of source code.

**Key question:** Why `message.content[0].text`?
**Answer:** Claude wraps responses in a list because a response can contain 
multiple content blocks (text, images, tool calls). `[0]` gets the first 
block which is always the text in simple calls.

### script8_ask.py
Interactive CLI — user types a question, Claude answers.
**Key question:** What does `input()` do?
**Answer:** Pauses the program and waits for the user to type something 
in the terminal. Returns what they typed as a string which gets passed 
directly to Claude as the question.

**Key question:** What is `\n` in the print statement?
**Answer:** A newline character that creates a blank line between the 
label and Claude's response. Makes terminal output easier to read.

**Key insight:** When asked for real-time data (flights, prices, live scores) 
Claude admits it doesn't know and redirects. This honest behaviour is exactly 
what we'll measure with eval suites in Week 6.

### script9_fastapi.py
Wraps the Claude question-answering logic from script8 in a real HTTP API
using FastAPI and Pydantic. First service in this repo that anything other
than the terminal can call.

**Key question:** What does `@app.post("/ask")` actually do?
**Answer:** A decorator is a function that wraps another function to add behaviour. `@app.post("/ask")` registers the function below it as the handler for POST requests to /ask — FastAPI's internal route table gets updated automatically. The `response_model=AskResponse` argument also tells FastAPI to validate the return value against the `AskResponse` model before sending it back, so validation runs on both edges of the endpoint.

**Key question:** Why is `client = anthropic.Client(...)` outside the
function and not inside?
**Answer:** Module-level code runs once when uvicorn imports the file. Function-body code runs on every request. The Anthropic client is reusable — its construction sets up connection pools, TLS, and retry logic. Building it once at startup and reusing it for every request is the right pattern. Building it inside the function would re-initialise all that state on every call, which gets expensive fast at any real traffic level.

**Key question:** What does `Field(..., min_length=1, max_length=1000)`
do, and why the three dots?
**Answer:** The `...` (called `Ellipsis`) means "this field is required — no default value." If a real default were there instead, the field would become optional. `min_length=1` rejects empty strings before they reach Claude — no point paying for an empty API call. `max_length=1000` rejects suspiciously long input — protects against runaway costs and abuse. All four rules are enforced before your function ever runs.

**Key insight:** The auto-generated `/docs` page is built from the same Pydantic models that validate requests at runtime. Code, validation, and docs all come from one source — they can't drift apart because they can't disagree. This is the pattern OpenAI and Anthropic use for their own APIs. It's why FDE job descriptions name Pydantic specifically.

## JS → Python concepts learned

| JavaScript | Python | Note |
|------------|--------|------|
| Array `[]` | List `[]` | Same syntax, different name |
| Object `{}` | Dictionary `{}` | Same concept |
| No strict types | Strict types | Python throws TypeError, JS silently coerces |
| `Object.entries()` | `.items()` | Python's tuple unpacking is cleaner |
| Any function result | `return` | Must explicitly return to get value back |
| `toFixed(2)` | `f"{value:.2f}"` | Format float to 2 decimal places |
| template literals `` ` `` | f-strings `f""` | Same concept, different syntax |
| `fetch(url).then(r => r.json())` | `requests.get(url).json()` | HTTP GET + parse response |
| `app.post('/x', fn)` (Express) | `@app.post("/x")` decorator (FastAPI) | Decorator syntax keeps the route declaration next to the handler function |
| Manual JSON validation with Joi/Zod | `class X(BaseModel)` declaration | Pydantic validates request and response automatically from the type declaration |
| `new Anthropic(...)` | `anthropic.Client(...)` | Python has no `new` keyword — calling the class IS the constructor |