#!/usr/bin/env python3
"""
Step 8: Agent Teams
Multiple agents with different roles communicating via message passing.
What's new: threaded workers with file-based inboxes.
Focus: inter-agent message flow.
"""
import json
import os
import subprocess
import threading
import time
from dotenv import load_dotenv
from openai import OpenAI
from display import print_thinking, BLUE, GREEN, YELLOW, DIM, CYAN, MAGENTA, RESET

load_dotenv()

client = OpenAI(api_key=os.getenv("MINIMAX_API_KEY"), base_url="https://api.minimax.chat/v1")
MODEL = "MiniMax-M2.7"

BLUE = "\033[94m"; GREEN = "\033[92m"; YELLOW = "\033[93m"; DIM = "\033[2m"; RESET = "\033[0m"
CYAN = "\033[96m"; MAGENTA = "\033[95m"

TEAM_DIR = ".team_inbox"
os.makedirs(TEAM_DIR, exist_ok=True)
_inbox_lock = threading.Lock()


def send_message(from_agent, to_agent, content):
    path = os.path.join(TEAM_DIR, f"{to_agent}.jsonl")
    with _inbox_lock:
        with open(path, "a") as f:
            f.write(json.dumps({"from": from_agent, "content": content}) + "\n")
    print(f"  {MAGENTA}[Mail] {from_agent} -> {to_agent}: {content[:80]}{RESET}")
    return f"Message sent to {to_agent}"

def read_inbox(agent_name):
    path = os.path.join(TEAM_DIR, f"{agent_name}.jsonl")
    with _inbox_lock:
        if not os.path.exists(path): return "Inbox empty."
        with open(path) as f: lines = f.readlines()
        open(path, "w").close()
    if not lines: return "Inbox empty."
    msgs = []
    for l in lines:
        m = json.loads(l)
        msgs.append(f"[From {m['from']}]: {m['content']}")
    print(f"  {MAGENTA}[Mail] {agent_name} inbox: {len(msgs)} message(s){RESET}")
    return "\n".join(msgs)


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


def run_worker(name, role, max_turns=15):
    worker_tools = [
        {"type": "function", "function": {"name": "run_bash",      "description": "Run a bash command.", "parameters": {"type": "object", "properties": {"command": {"type": "string"}},                             "required": ["command"]}}},
        {"type": "function", "function": {"name": "read_file",     "description": "Read a file.",        "parameters": {"type": "object", "properties": {"path": {"type": "string"}},                               "required": ["path"]}}},
        {"type": "function", "function": {"name": "write_file",    "description": "Write to a file.",    "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
        {"type": "function", "function": {"name": "read_inbox",     "description": "Read your inbox.",    "parameters": {"type": "object", "properties": {}}}},
        {"type": "function", "function": {"name": "send_message",   "description": "Send a message.",     "parameters": {"type": "object", "properties": {"to_agent": {"type": "string"}, "content": {"type": "string"}}, "required": ["to_agent", "content"]}}},
    ]
    handlers = {
        "run_bash":     lambda args: run_bash(args["command"]),
        "read_file":    lambda args: read_file(args["path"]),
        "write_file":   lambda args: write_file(args["path"], args["content"]),
        "read_inbox":   lambda args: read_inbox(name),
        "send_message": lambda args: send_message(name, args["to_agent"], args["content"]),
    }
    msgs = [
        {"role": "system", "content": f"You are '{name}'. Role: {role}\n\nStart by reading your inbox for instructions. When done, send a message to 'lead' summarizing what you did."},
        {"role": "user", "content": "Begin. Check your inbox first."},
    ]

    print(f"  {CYAN}[{name}] Worker started (role: {role}){RESET}")

    for turn in range(max_turns):
        response = client.chat.completions.create(model=MODEL, messages=msgs, tools=worker_tools)
        msg = response.choices[0].message
        msgs.append(msg)
        if not msg.tool_calls:
            print(f"  {CYAN}[{name}] Done ({turn+1} turns){RESET}")
            return
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            fn = tc.function.name
            if fn in ("send_message", "read_inbox"):
                result = handlers[fn](args)
            else:
                print(f"    {DIM}[{name}] {fn}({json.dumps(args, ensure_ascii=False)[:60]}){RESET}")
                result = handlers[fn](args)
            msgs.append({"role": "tool", "tool_call_id": tc.id, "content": result[:2000]})

    print(f"  {CYAN}[{name}] Reached max turns{RESET}")


worker_threads = []

def spawn_worker(name, role):
    t = threading.Thread(target=run_worker, args=(name, role), daemon=True)
    worker_threads.append(t)
    t.start()
    return f"Worker '{name}' spawned."

def wait_for_workers():
    print(f"\n  {DIM}Waiting for all workers to finish...{RESET}")
    for t in worker_threads: t.join(timeout=120)
    worker_threads.clear()
    return "All workers finished.\n" + read_inbox("lead")


lead_tools = [
    {"type": "function", "function": {"name": "run_bash",         "description": "Run a bash command.",                  "parameters": {"type": "object", "properties": {"command": {"type": "string"}},                              "required": ["command"]}}},
    {"type": "function", "function": {"name": "read_file",        "description": "Read a file.",                         "parameters": {"type": "object", "properties": {"path": {"type": "string"}},                                "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file",       "description": "Write to a file.",                    "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},  "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "send_message",     "description": "Send a message to a worker's inbox.", "parameters": {"type": "object", "properties": {"to_agent": {"type": "string"}, "content": {"type": "string"}}, "required": ["to_agent", "content"]}}},
    {"type": "function", "function": {"name": "read_inbox",       "description": "Read your own inbox.",                "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "spawn_worker",   "description": "Spawn a worker agent.",               "parameters": {"type": "object", "properties": {"name": {"type": "string"}, "role": {"type": "string"}},     "required": ["name", "role"]}}},
    {"type": "function", "function": {"name": "wait_for_workers","description": "Wait for all workers to finish.",     "parameters": {"type": "object", "properties": {}}}},
]

lead_handlers = {
    "run_bash":         lambda args: run_bash(args["command"]),
    "read_file":        lambda args: read_file(args["path"]),
    "write_file":       lambda args: write_file(args["path"], args["content"]),
    "send_message":     lambda args: send_message("lead", args["to_agent"], args["content"]),
    "read_inbox":       lambda args: read_inbox("lead"),
    "spawn_worker":     lambda args: spawn_worker(args["name"], args["role"]),
    "wait_for_workers": lambda args: wait_for_workers(),
}

SYSTEM_PROMPT = """You are the lead agent coordinating a team.

Workflow:
1. send_message to each worker's inbox with clear instructions
2. spawn_worker for each worker (they read their inbox automatically)
3. wait_for_workers — blocks until all finish, then shows their reports
4. Summarize results to the user"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("=" * 50)
print("Step 8: Agent Teams")
print('Sample: "Build a calculator web app in step08_team/:')
print('         backend in Python, frontend in HTML."')
print("=" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    messages.append({"role": "user", "content": user_input})

    turn = 0
    while True:
        turn += 1
        print(f"\n{BLUE}═══ Lead Turn {turn} ═══════════════════════{RESET}")

        response = client.chat.completions.create(model=MODEL, messages=messages, tools=lead_tools)
        choice = response.choices[0]
        msg = choice.message
        messages.append(msg)

        print(f"  {DIM}finish_reason: {choice.finish_reason}{RESET}")

        if not msg.tool_calls:
            print_thinking(msg.content, label="Lead")
            break

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            if name in ("send_message", "read_inbox", "spawn_worker", "wait_for_workers"):
                result = lead_handlers[name](args)
            else:
                print(f"  {YELLOW}→ tool: {name}({json.dumps(args, ensure_ascii=False)[:80]}){RESET}")
                result = lead_handlers[name](args)
                print(f"  {DIM}  = {result[:150]}{RESET}")

            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
