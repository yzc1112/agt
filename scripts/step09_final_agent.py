#!/usr/bin/env python3
"""
Step 9: The Final Agent
Combines everything from Steps 3-6 into one powerful agent:
  - Tools: run_bash, read_file, write_file
  - Planning: todo_add, todo_update, todo_list
  - Memory: save_memory, recall_memory, list_memories
Skips subagent/team (Steps 7-8) for a clean, single-agent final product.
"""
import glob
import json
import os
import subprocess
from config import client, MODEL
from display import print_thinking, BLUE, GREEN, YELLOW, DIM, CYAN, MAGENTA, RESET

PROJECT_DIR = "word_freq_project"
os.makedirs(PROJECT_DIR, exist_ok=True)

# ── Memory ──────────────────────────────────────────────────────────────────────
MEMORY_DIR = ".final_agent_memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

def save_memory(key, content):
    path = os.path.join(MEMORY_DIR, f"{key}.md")
    with open(path, "w") as f: f.write(content)
    print(f"  {MAGENTA}[Memory] saved '{key}'{RESET}")
    return f"Saved '{key}'"

def recall_memory(query):
    results = []
    for path in glob.glob(os.path.join(MEMORY_DIR, "*.md")):
        with open(path) as f: content = f.read()
        key = os.path.basename(path).replace(".md", "")
        if query.lower() in content.lower() or query.lower() in key.lower():
            results.append(f"[{key}]: {content}")
    print(f"  {MAGENTA}[Memory] recall '{query}' -> {len(results)} match(es){RESET}")
    return "\n".join(results) if results else "No matching memories."

def list_memories():
    files = glob.glob(os.path.join(MEMORY_DIR, "*.md"))
    keys = [os.path.basename(f).replace(".md", "") for f in files]
    print(f"  {MAGENTA}[Memory] saved: {keys if keys else '(none)'}{RESET}")
    return "Saved: " + ", ".join(keys) if keys else "No memories saved."

# ── Todo ────────────────────────────────────────────────────────────────────────
todos = []

def todo_add(task):
    todos.append({"id": len(todos) + 1, "task": task, "status": "pending"})
    return f"Added #{todos[-1]['id']}: {task}"

def todo_update(todo_id, status):
    for t in todos:
        if t["id"] == todo_id:
            t["status"] = status
            return f"#{todo_id} -> {status}"
    return f"#{todo_id} not found"

def todo_list():
    if not todos: return "No todos."
    return "\n".join(f"  #{t['id']} [{t['status']}] {t['task']}" for t in todos)

def show_todos():
    if not todos: return
    icons = {"pending": " ", "in_progress": "~", "completed": "x"}
    print(f"  {CYAN}── Todos ────────────────────────────────{RESET}")
    for t in todos:
        print(f"  {CYAN}  [{icons[t['status']]}] #{t['id']} {t['task']}{RESET}")

# ── Tools ──────────────────────────────────────────────────────────────────────
tools = [
    {"type": "function", "function": {"name": "run_bash",       "description": "Run a bash command.",                   "parameters": {"type": "object", "properties": {"command": {"type": "string"}},                              "required": ["command"]}}},
    {"type": "function", "function": {"name": "read_file",      "description": "Read a file.",                           "parameters": {"type": "object", "properties": {"path": {"type": "string"}},                                "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file",     "description": "Write to a file.",                        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},  "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "save_memory",    "description": "Save info to persistent memory.",           "parameters": {"type": "object", "properties": {"key": {"type": "string"}, "content": {"type": "string"}},   "required": ["key", "content"]}}},
    {"type": "function", "function": {"name": "recall_memory",  "description": "Search memories by keyword.",              "parameters": {"type": "object", "properties": {"query": {"type": "string"}},                               "required": ["query"]}}},
    {"type": "function", "function": {"name": "list_memories", "description": "List all saved memory keys.",              "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "todo_add",      "description": "Add a todo item.",                        "parameters": {"type": "object", "properties": {"task": {"type": "string"}},                              "required": ["task"]}}},
    {"type": "function", "function": {"name": "todo_update",   "description": "Update a todo status.",                   "parameters": {"type": "object", "properties": {"todo_id": {"type": "integer"}, "status": {"type": "string", "enum": ["pending", "in_progress", "completed"]}}, "required": ["todo_id", "status"]}}},
    {"type": "function", "function": {"name": "todo_list",     "description": "List all todos.",                        "parameters": {"type": "object", "properties": {}}}},
]

def run_bash(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
    return (result.stdout + result.stderr).strip() or "(no output)"

def read_file(path):
    try:
        with open(path) as f: return f.read()
    except FileNotFoundError:
        return f"Error: {path} not found"

def write_file(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f: f.write(content)
    return f"Written to {path}"

TOOL_HANDLERS = {
    "run_bash":      lambda a: run_bash(a["command"]),
    "read_file":     lambda a: read_file(a["path"]),
    "write_file":    lambda a: write_file(a["path"], a["content"]),
    "save_memory":   lambda a: save_memory(a["key"], a["content"]),
    "recall_memory": lambda a: recall_memory(a["query"]),
    "list_memories": lambda a: list_memories(),
    "todo_add":      lambda a: todo_add(a["task"]),
    "todo_update":   lambda a: todo_update(a["todo_id"], a["status"]),
    "todo_list":     lambda a: todo_list(),
}

SYSTEM_PROMPT = """You are a capable coding agent with planning and persistent memory.

Capabilities:
- run_bash, read_file, write_file: file and shell operations
- save_memory/recall_memory/list_memories: persistent memory across sessions
- todo_add/todo_update/todo_list: plan and track tasks

Guidelines:
- For complex tasks: plan first with todos, then execute step by step
- For important user preferences: save to memory so you remember them across sessions
- At the start of conversation: use list_memories to check what you already know"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("=" * 60)
print("Step 9: The Final Agent")
print("  Tools: bash, read/write files, memory, todos")
print()
print("  === ITERATION 1 ===")
print("  You: Set up a word_freq project in word_freq_project/:")
print("        Create word_freq.py that reads a text file and prints")
print("        word frequencies sorted by count, as a table (Word | Count | %).")
print("        Save preference: always show as table.")
print("        Create sample.txt with 3 programming sentences.")
print("        Run word_freq.py on sample.txt.")
print()
print("  === ITERATION 2 ===")
print('  You: Run word_freq.py on sample.txt again.')
print("        (agent recalls the table format preference from memory)")
print("=" * 60)

while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    messages.append({"role": "user", "content": user_input})

    turn = 0
    while True:
        turn += 1
        print(f"\n  {BLUE}-- Turn {turn} ------------------------------------------{RESET}")

        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        choice = response.choices[0]
        msg = choice.message
        messages.append(msg)

        print(f"  {DIM}  finish_reason: {choice.finish_reason}{RESET}")

        if not msg.tool_calls:
            print_thinking(msg.content)
            break

        had_mutating = False
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  {YELLOW}  → {name}({json.dumps(args, ensure_ascii=False)[:80]}){RESET}")
            result = TOOL_HANDLERS[name](args)
            print(f"  {DIM}    = {result[:200]}{RESET}")
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
            if name in ("todo_add", "todo_update"):
                had_mutating = True

        # Inject todo state AFTER all tool results so model sees it in next turn
        if had_mutating:
            todo_state = json.dumps({"todos": todos}, indent=2)
            messages.append({"role": "user", "content": f"[Todo State Updated]\n{todo_state}"})

        show_todos()
