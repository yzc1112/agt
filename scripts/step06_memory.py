#!/usr/bin/env python3
"""
Step 6: An Agent That Remembers
File-based memory that persists across sessions.
What's new: save_memory / recall_memory using .agent_memory/ directory.
Focus: persistence — run twice to see memory carry over.
"""
import glob
import json
import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI
from display import print_thinking, BLUE, GREEN, YELLOW, DIM, MAGENTA, RESET

load_dotenv()

client = OpenAI(api_key=os.getenv("MINIMAX_API_KEY"), base_url="https://api.minimax.chat/v1")
MODEL = "MiniMax-M2.7"


MEMORY_DIR = ".agent_memory"
os.makedirs(MEMORY_DIR, exist_ok=True)


def save_memory(key, content):
    path = os.path.join(MEMORY_DIR, f"{key}.md")
    with open(path, "w") as f: f.write(content)
    print(f"  {MAGENTA}[Memory] Saved to {path}{RESET}")
    return f"Saved memory '{key}'"

def recall_memory(query):
    results = []
    for path in glob.glob(os.path.join(MEMORY_DIR, "*.md")):
        with open(path) as f: content = f.read()
        key = os.path.basename(path).replace(".md", "")
        if query.lower() in content.lower() or query.lower() in key.lower():
            results.append(f"[{key}]: {content}")
    found = "\n".join(results) if results else "No matching memories found."
    print(f"  {MAGENTA}[Memory] Recall '{query}' -> {len(results)} match(es){RESET}")
    return found

def list_memories():
    files = glob.glob(os.path.join(MEMORY_DIR, "*.md"))
    if not files: return "No memories saved yet."
    keys = [os.path.basename(f).replace(".md", "") for f in files]
    print(f"  {MAGENTA}[Memory] Files in {MEMORY_DIR}/: {keys}{RESET}")
    return "Saved memories: " + ", ".join(keys)


tools = [
    {"type": "function", "function": {"name": "run_bash",       "description": "Run a bash command.",                        "parameters": {"type": "object", "properties": {"command": {"type": "string"}},                              "required": ["command"]}}},
    {"type": "function", "function": {"name": "read_file",      "description": "Read a file.",                                "parameters": {"type": "object", "properties": {"path": {"type": "string"}},                                "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file",     "description": "Write to a file.",                           "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},  "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "save_memory",    "description": "Save info to persistent memory with a key.", "parameters": {"type": "object", "properties": {"key": {"type": "string"}, "content": {"type": "string"}},   "required": ["key", "content"]}}},
    {"type": "function", "function": {"name": "recall_memory",  "description": "Search memories by keyword.",                "parameters": {"type": "object", "properties": {"query": {"type": "string"}},                               "required": ["query"]}}},
    {"type": "function", "function": {"name": "list_memories",  "description": "List all saved memory keys.",                "parameters": {"type": "object", "properties": {}}}},
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
    "run_bash":      lambda args: run_bash(args["command"]),
    "read_file":     lambda args: read_file(args["path"]),
    "write_file":    lambda args: write_file(args["path"], args["content"]),
    "save_memory":   lambda args: save_memory(args["key"], args["content"]),
    "recall_memory": lambda args: recall_memory(args["query"]),
    "list_memories": lambda args: list_memories(),
}

SYSTEM_PROMPT = """You are a helpful assistant with persistent memory.

At the start of each conversation, use list_memories to check what you already know.
Use save_memory to store user preferences or project details across sessions."""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("=" * 50)
print("Step 6: An Agent That Remembers")
print()
print("  === ITERATION 1 ===")
print("  You: My favorite color is blue. Remember this.")
print("         Also save this fact file_prefs: I prefer .md files.")
print()
print("  === ITERATION 2 (restart script first!) ===")
print('  You: What are my preferences? (check memory, then answer)')
print("=" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    messages.append({"role": "user", "content": user_input})

    turn = 0
    while True:
        turn += 1
        print(f"\n{BLUE}═══ Turn {turn} ══════════════════════════════{RESET}")

        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        choice = response.choices[0]
        msg = choice.message
        messages.append(msg)

        print(f"  {DIM}finish_reason: {choice.finish_reason}{RESET}")

        if not msg.tool_calls:
            print_thinking(msg.content)
            break

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  {YELLOW}→ tool: {name}({json.dumps(args, ensure_ascii=False)[:100]}){RESET}")
            result = TOOL_HANDLERS[name](args)
            print(f"  {DIM}  = {result[:150]}{RESET}")
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
