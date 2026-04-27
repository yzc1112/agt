#!/usr/bin/env python3
"""
Step 5: An Agent That Plans
Add todo/task tools so the agent plans before acting.
What's new: todo_add, todo_update, todo_list, todo_delete. Focus: planning behavior.
"""
import json
import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI
from display import print_thinking, BLUE, GREEN, YELLOW, DIM, CYAN, RESET

load_dotenv()

client = OpenAI(api_key=os.getenv("MINIMAX_API_KEY"), base_url="https://api.minimax.chat/v1")
MODEL = "MiniMax-M2.7"


# --- Todo List (in-memory) ---
todos = []

def todo_add(task):
    todos.append({"id": len(todos) + 1, "task": task, "status": "pending"})
    return f"Added todo #{todos[-1]['id']}: {task}"

def todo_update(todo_id, status):
    for t in todos:
        if t["id"] == todo_id:
            t["status"] = status
            return f"Todo #{todo_id} -> {status}"
    return f"Todo #{todo_id} not found"

def todo_list():
    if not todos: return "No todos yet."
    return "\n".join(f"  #{t['id']} [{t['status']}] {t['task']}" for t in todos)

def todo_delete(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return f"Todo #{todo_id} deleted"

def show_todos():
    if not todos: return
    icons = {"pending": " ", "in_progress": "~", "completed": "x"}
    print(f"  {CYAN}── Todo State ──────────────────────────{RESET}")
    for t in todos:
        print(f"  {CYAN}  [{icons[t['status']]}] #{t['id']} {t['task']}{RESET}")


tools = [
    {"type": "function", "function": {"name": "run_bash",     "description": "Run a bash command.",   "parameters": {"type": "object", "properties": {"command": {"type": "string"}},                                                   "required": ["command"]}}},
    {"type": "function", "function": {"name": "read_file",    "description": "Read a file.",           "parameters": {"type": "object", "properties": {"path": {"type": "string"}},                                                     "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file",   "description": "Write to a file.",       "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},                      "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "todo_add",     "description": "Add a todo item.",       "parameters": {"type": "object", "properties": {"task": {"type": "string"}},                                                     "required": ["task"]}}},
    {"type": "function", "function": {"name": "todo_update",  "description": "Update a todo status.",  "parameters": {"type": "object", "properties": {"todo_id": {"type": "integer"}, "status": {"type": "string", "enum": ["pending", "in_progress", "completed"]}}, "required": ["todo_id", "status"]}}},
    {"type": "function", "function": {"name": "todo_list",    "description": "List all todos.",        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "todo_delete",  "description": "Delete a todo by id.",   "parameters": {"type": "object", "properties": {"todo_id": {"type": "integer"}},                                              "required": ["todo_id"]}}},
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
    "run_bash":    lambda args: run_bash(args["command"]),
    "read_file":   lambda args: read_file(args["path"]),
    "write_file":  lambda args: write_file(args["path"], args["content"]),
    "todo_add":    lambda args: todo_add(args["task"]),
    "todo_update": lambda args: todo_update(args["todo_id"], args["status"]),
    "todo_list":   lambda args: todo_list(),
    "todo_delete": lambda args: todo_delete(args["todo_id"]),
}

SYSTEM_PROMPT = """You are a helpful coding agent with planning capabilities.

Before starting any complex task:
1. Use todo_add to break it into small steps
2. Use todo_update to mark steps in_progress / completed as you go

Always plan first, then execute."""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("=" * 50)
print("Step 5: An Agent That Plans")
print('Sample: "Set up a new Python project(new folder) with a calculator module and tests. Please plan first"')
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

        had_mutating = False
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  {YELLOW}→ tool: {name}({json.dumps(args, ensure_ascii=False)[:100]}){RESET}")
            result = TOOL_HANDLERS[name](args)
            print(f"  {DIM}  = {result[:150]}{RESET}")
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
            if name in ("todo_add", "todo_update", "todo_delete"):
                had_mutating = True

        # Inject todo state AFTER all tool results so model sees it in next turn
        if had_mutating:
            todo_state = json.dumps({"todos": todos}, indent=2)
            messages.append({"role": "user", "content": f"[Todo State Updated]\n{todo_state}"})

        show_todos()