# Step-by-Step Agent Building Workshop

A hands-on workshop that builds an AI agent from scratch, one concept per step. Each step is a self-contained Python file you can run live during the presentation.

---

## Setup

**1. Install dependencies**
```bash
pip install openai python-dotenv
```

**2. Create a `.env` file** in this directory:
```
MINIMAX_API_KEY=your-key-here
```

**3. Run any step**
```bash
python3 step01_hello_llm.py
```

> **Switching providers:** Every file has a 2-line block at the top. Change `api_key`, `base_url`, and `MODEL` to use any OpenAI-compatible API (OpenAI, Ollama, DeepSeek, etc.).
> ```python
> client = OpenAI(api_key=..., base_url=...)
> MODEL = "..."
> ```

---

## The 8 Steps

### Step 1 — Hello, LLM (`step01_hello_llm.py`)
**Concept:** Connect to a model and get one response.

```
You: [your question]
Assistant: [response]
```

**What's happening:** One API call. Input → LLM → Output. That's the atom of everything that follows.

---

### Step 2 — The Conversation Loop (`step02_chat_loop.py`)
**Concept:** A `while True` loop turns a single call into a chatbot.

```
You: What is Python?
Assistant: Python is ...

You: Give me an example
Assistant: Sure, here's ...   ← remembers the previous message
```

**What's new:** Message history is accumulated and sent on every call. The LLM has no memory — *we* give it context by replaying the history.

**Key pattern:**
```python
messages.append({"role": "user", "content": user_input})
response = client.chat.completions.create(model=MODEL, messages=messages)
messages.append({"role": "assistant", "content": response...content})
```

---

### Step 3 — Tool Use (`step03_tool_use.py`)
**Concept:** Give the LLM a tool (bash), let it call the tool, return the result.

```
You: What files are in the current directory?
[Tool] run_bash(ls -la)
[Result] step01_hello_llm.py  step02_chat_loop.py ...
Assistant: The directory contains 8 Python files ...
```

**What's new:** Tool definitions tell the LLM what it *can* do. When it responds with `tool_calls` instead of text, we execute the tool and feed the result back.

**Key pattern:**
```python
if msg.tool_calls:
    result = run_bash(args["command"])
    messages.append({"role": "tool", "content": result})
    response = client.chat.completions.create(...)   # call again with result
```

---

### Step 4 — The Agent Loop (`step04_agent_loop.py`)
**Concept:** The agent keeps calling tools until it decides it's done.

```
You: Create hello.txt with a poem, then read it back
  [Tool] write_file(hello.txt, ...)
  [Tool] read_file(hello.txt)
Assistant: Done! Here's the poem: ...
```

**What's new:** Instead of one round-trip, we loop: `call LLM → execute tools → call LLM again → ...` until `tool_calls` is empty. The agent chains its own actions.

**Key pattern:**
```python
while True:
    response = client.chat.completions.create(...)
    if not msg.tool_calls:
        break          # agent decided it's done
    for tool_call in msg.tool_calls:
        ...            # execute, append result, loop again
```

**Tools available:** `run_bash`, `read_file`, `write_file`

---

### Step 5 — Planning (`step05_planning.py`)
**Concept:** Add todo tools so the agent plans before acting.

```
You: Set up a Python project with a calculator and tests
  [Tool] todo_add(Create project structure)
  [Tool] todo_add(Write calculator.py)
  [Tool] todo_add(Write test_calculator.py)
  [Tool] todo_update(#1 → in_progress)
  [Tool] run_bash(mkdir calculator_project)
  ...
```

**What's new:** `todo_add`, `todo_update`, `todo_list` tools + a system prompt that instructs the agent to plan first. Visible state makes the agent more reliable and easier to follow.

**Key insight:** The agent doesn't become smarter — it just has a structure that forces it to think step by step.

---

### Step 6 — Memory (`step06_memory.py`)
**Concept:** File-based memory that persists across sessions.

```bash
# Session 1
You: Remember that I prefer pytest over unittest
  [Tool] save_memory(testing_preference, "I prefer pytest...")

# Session 2 (restart the script)
You: What testing framework do I prefer?
  [Tool] list_memories()
  [Tool] recall_memory(testing)
Assistant: You prefer pytest over unittest.
```

**What's new:** `save_memory` writes to `.agent_memory/key.md`. `recall_memory` searches them by keyword. Memory = files. Simple but persistent.

---

### Step 7 — Subagents (`step07_subagent.py`)
**Concept:** Spawn a child agent with a focused task and clean context.

```
You: Research the top 3 Python web frameworks, write a comparison to frameworks.md
  [Tool] spawn_subagent(Research top 3 Python web frameworks and write to frameworks.md)
    [Sub-Tool] run_bash(...)
    [Sub-Tool] write_file(frameworks.md, ...)
  [Subagent] Done in 3 turns
Assistant: The sub-agent completed the research and wrote frameworks.md
```

**What's new:** `spawn_subagent` creates a fresh agent loop with empty message history. The parent only sees a text summary — the sub-agent's tool calls don't clutter the parent's context.

**Key insight:** "Process isolation gives context isolation for free." Use subagents for research, isolated file work, or anything that would bloat the parent's history.

---

### Step 8 — Agent Teams (`step08_team.py`)
**Concept:** Multiple agents with roles, communicating via message passing.

```
You: Build a calculator web app — backend in Python, frontend in HTML
  [Lead] send_message(backend, "Write a Flask API for a calculator...")
  [Lead] send_message(frontend, "Write HTML/JS for a calculator UI...")
  [Lead] spawn_worker(backend, "backend developer")
  [Lead] spawn_worker(frontend, "frontend developer")
  [Lead] wait_for_workers()
    [backend] read_inbox()  → gets instructions
    [backend] write_file(app.py, ...)
    [frontend] read_inbox() → gets instructions
    [frontend] write_file(index.html, ...)
  [Lead] All workers finished.
Assistant: The team completed the app — app.py and index.html are ready.
```

**What's new:** Workers run in parallel threads. Each has its own inbox (a `.jsonl` file). The lead sends instructions, spawns workers, then waits. Workers report back via `send_message("lead", ...)`.

**Key insight:** Agents coordinate through simple file-based message queues. No shared state — just messages.

---

## Understanding the Debug Output

Every step prints **educational debug output** showing what happens under the hood. Each step focuses on its **own new concept** — once a concept is taught, subsequent steps abbreviate it.

### Color legend

| Color | Meaning |
|-------|---------|
| Blue `───` | **REQUEST** — what we're about to send to the model (message count, roles, tools) |
| Green `───` | **RESPONSE** — what the model returned (`finish_reason`, `tool_calls` or `content`) |
| Yellow `───` | **APPEND** — the exact dict we add to `messages[]` |
| Cyan `│` | **Subagent / Worker** — isolated context or team member activity |
| Magenta `[Mail]` / `[Memory]` | **Message passing** or **memory operations** |
| Dim | Supplementary info (result previews, turn counters) |

### What each step highlights

| Step | Debug focus |
|------|-------------|
| 01 | Raw response object: `model`, `finish_reason`, `usage` (tokens) |
| 02 | Message history growth: `[sending 3 messages: system -> user -> assistant -> user]` |
| 03 | **Full tool call protocol** — REQUEST/RESPONSE/APPEND for both rounds |
| 04 | Agent loop turns: `Turn 1`, `Turn 2`... + abbreviated tool calls |
| 05 | Todo state display after each round: `[ ] #1 Create project`, `[x] #2 Write module` |
| 06 | Memory file operations: `[Memory] Saved to .agent_memory/testing.md` |
| 07 | Context isolation: `Subagent messages: 2 (fresh! parent has 8)` |
| 08 | Message passing: `[Mail] lead -> backend: Write a Flask API...` |

### Example: Step 3 output (the key teaching moment)

```
─── REQUEST ──────────────────────────────     ← what we send
  Messages: 2 [system -> user]
  Tools:    ['run_bash']

─── RESPONSE ─────────────────────────────     ← what the model returns
  finish_reason: tool_calls                    ← "I want to call a tool"
  content: null                                ← no text yet
  tool_calls:
    [0] id       = call_abc123
        function = run_bash                    ← which tool
        arguments= {"command": "ls -la"}       ← with what args

>>> Executing: run_bash(ls -la)                ← we run it
>>> Result: step01_hello_llm.py ...

─── APPEND: tool result ──────────────────     ← we feed result back
  {"role": "tool", "tool_call_id": "call_abc123", "content": "..."}

─── REQUEST ──────────────────────────────     ← round 2
  Messages: 4 [system -> user -> assistant -> tool]

─── RESPONSE ─────────────────────────────
  finish_reason: stop                          ← "I'm done, here's my answer"
  content: "The current directory contains..."
```

---

## Concept Progression

```
Step 1   input → LLM → output
Step 2   + loop + history              = chatbot
Step 3   + tools                       = tool-using assistant
Step 4   + agent loop                  = autonomous agent
Step 5   + planning (todos)            = structured agent
Step 6   + memory (files)              = persistent agent
Step 7   + subagents                   = delegating agent
Step 8   + team + message passing      = multi-agent system
```

Each step adds **one idea**. The loop from Step 4 appears unchanged in every subsequent step.

---

## Suggested Demo Flow

| Step | Ask the agent... |
|------|-----------------|
| 01 | `What is an AI agent?` |
| 02 | `What is Python?` then `Give me an example` (shows memory) |
| 03 | `What files are in the current directory?` |
| 04 | `Create hello.txt with a poem, then read it back` |
| 05 | `Set up a Python project with a calculator module and tests` |
| 06 | `Remember I prefer pytest` → restart → `What test framework do I prefer?` |
| 07 | `Research the top 3 Python web frameworks and write a comparison to frameworks.md` |
| 08 | `Build a simple calculator web app — backend in Python, frontend in HTML` |
