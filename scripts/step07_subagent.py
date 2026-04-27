#!/usr/bin/env python3
"""
Step 7: Divide and Conquer — Subagents
Spawn a child agent with a focused task and clean context.
What's new: spawn_subagent — runs a fresh agent loop, returns a summary.
Focus: context isolation (parent vs subagent message counts).
"""
import json
import os
import subprocess
from config import client, MODEL
from display import print_thinking, BLUE, GREEN, YELLOW, DIM, CYAN, RESET


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


BASIC_TOOLS = [
    {"type": "function", "function": {"name": "run_bash",   "description": "Run a bash command.", "parameters": {"type": "object", "properties": {"command": {"type": "string"}},                             "required": ["command"]}}},
    {"type": "function", "function": {"name": "read_file",  "description": "Read a file.",        "parameters": {"type": "object", "properties": {"path": {"type": "string"}},                               "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file", "description": "Write to a file.",    "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
]

BASIC_HANDLERS = {
    "run_bash":   lambda args: run_bash(args["command"]),
    "read_file":  lambda args: read_file(args["path"]),
    "write_file": lambda args: write_file(args["path"], args["content"]),
}


def run_subagent(task, max_turns=10):
    """Spawn a child agent with a FRESH context."""
    sub_messages = [
        {"role": "system", "content": "You are a focused sub-agent. Complete the task, then summarize what you did."},
        {"role": "user", "content": task},
    ]

    print(f"\n  {CYAN}┌── Subagent Spawned ──────────────────────{RESET}")
    print(f"  {CYAN}│ Task: {task[:70]}{RESET}")
    print(f"  {CYAN}│ Messages: {len(sub_messages)} (fresh! parent has {len(messages)}){RESET}")
    print(f"  {CYAN}│ Tools: {[t['function']['name'] for t in BASIC_TOOLS]}{RESET}")

    for turn in range(max_turns):
        response = client.chat.completions.create(model=MODEL, messages=sub_messages, tools=BASIC_TOOLS)
        msg = response.choices[0].message
        sub_messages.append(msg)

        if not msg.tool_calls:
            print(f"  {CYAN}│ Done in {turn + 1} turns (subagent msgs: {len(sub_messages)}){RESET}")
            print(f"  {CYAN}└──────────────────────────────────────────{RESET}")
            return msg.content or "Subagent completed."

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  {CYAN}│  tool: {name}({json.dumps(args, ensure_ascii=False)[:60]}){RESET}")
            result = BASIC_HANDLERS[name](args)
            sub_messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result[:2000]})

    print(f"  {CYAN}└── Subagent hit max turns ────────────────{RESET}")
    return "Subagent reached max turns."


# --- Parent agent tools ---
parent_tools = BASIC_TOOLS + [
    {
        "type": "function",
        "function": {
            "name": "spawn_subagent",
            "description": "Spawn a sub-agent with a specific focused task. It runs with a clean context and returns a summary.",
            "parameters": {
                "type": "object",
                "properties": {"task": {"type": "string"}},
                "required": ["task"],
            },
        },
    },
]

PARENT_HANDLERS = {
    **BASIC_HANDLERS,
    "spawn_subagent": lambda args: run_subagent(args["task"]),
}

SYSTEM_PROMPT = """You are a lead agent that can delegate work to sub-agents.

Use spawn_subagent for research, isolated tasks, or anything that would clutter your own context.
You keep the big picture. Sub-agents handle the details."""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("=" * 50)
print("Step 7: Subagents — Divide and Conquer")
print('Sample: "Spawn 2 subagents in parallel to create:')
print('  - hello.txt ("Hello from subagent 1!")')
print('  - about.txt ("Made by subagent 2")')
print('Each subagent writes its own file independently."')
print("=" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    messages.append({"role": "user", "content": user_input})

    turn = 0
    while True:
        turn += 1
        print(f"\n{BLUE}═══ Turn {turn} (messages: {len(messages)}) ══{RESET}")

        response = client.chat.completions.create(model=MODEL, messages=messages, tools=parent_tools)
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
            print(f"  {YELLOW}→ tool: {name}({json.dumps(args, ensure_ascii=False)[:80]}){RESET}")
            result = PARENT_HANDLERS[name](args)
            if name != "spawn_subagent":
                print(f"  {DIM}  = {result[:150]}{RESET}")
            else:
                print(f"  {DIM}  subagent returned: {result[:200]}{RESET}")
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
