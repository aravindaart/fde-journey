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
