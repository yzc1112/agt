#!/usr/bin/env python3
"""
Step 4: The Agent Loop
The agent keeps calling tools until it decides to stop.
What's new: the inner while loop — agent chains tool calls autonomously.
Step 3 taught the tool call protocol; here we focus on the LOOP.
"""
import json
import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI
from display import print_thinking, BLUE, GREEN, YELLOW, DIM, RESET

load_dotenv()

client = OpenAI(api_key=os.getenv("MINIMAX_API_KEY"), base_url="https://api.minimax.chat/v1")
MODEL = "MiniMax-M2.7"


def show_messages(messages):
    for i, m in enumerate(messages):
        role = m["role"] if isinstance(m, dict) else m.role
        content = str(m.get("content") or "") if isinstance(m, dict) else str(m.content or "")
        preview = content[:70].replace("\n", " ")
        print(f"  {DIM}  [{i}] {role:10s}: \"{preview}{'...' if len(content) > 70 else ''}\"{RESET}")


tools = [
    {"type": "function", "function": {"name": "run_bash",   "description": "Run a bash command.",      "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}},
    {"type": "function", "function": {"name": "read_file",  "description": "Read a file.",             "parameters": {"type": "object", "properties": {"path": {"type": "string"}},    "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file", "description": "Write content to a file.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
]


AGT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_bash(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30, cwd=AGT_DIR)
    return (result.stdout + result.stderr).strip() or "(no output)"

def read_file(path):
    full = os.path.join(AGT_DIR, path)
    try:
        with open(full) as f: return f.read()
    except FileNotFoundError:
        return f"Error: {path} not found"

def write_file(path, content):
    full = os.path.join(AGT_DIR, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w") as f: f.write(content)
    return f"Written to {path} (resolved: {full})"

TOOL_HANDLERS = {
    "run_bash":   lambda args: run_bash(args["command"]),
    "read_file":  lambda args: read_file(args["path"]),
    "write_file": lambda args: write_file(args["path"], args["content"]),
}

messages = [
    {"role": "system", "content": "You are a helpful coding agent. Use your tools to accomplish tasks."},
]

print("=" * 50)
print("Step 4: The Agent Loop")
print('Sample: "Create step04_agent_loop/calculate.py to calculate 15412*53234 and output the result into step04_agent_loop/result.txt file. do not print the result out')
print('then run python3 and read the result.txt file to give me the result."')
print("=" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    messages.append({"role": "user", "content": user_input})

    # ── THE AGENT LOOP ─────────────────────────────────────────────────────────
    # Key difference from Step 3: we keep looping until finish_reason == "stop".
    turn = 0
    while True:
        turn += 1
        print(f"\n{BLUE}═══ Turn {turn} ══════════════════════════════{RESET}")
        print(f"  {DIM}messages[] ({len(messages)} items):{RESET}")
        show_messages(messages)

        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        choice = response.choices[0]
        msg = choice.message
        messages.append(msg)

        print(f"  {GREEN}finish_reason: {choice.finish_reason!r}{RESET}")

        if not msg.tool_calls:
            print(f"  {DIM}→ No tool calls. Agent is done.{RESET}")
            print_thinking(msg.content)
            break

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  {YELLOW}→ tool: {name}({json.dumps(args, ensure_ascii=False)[:100]}){RESET}")
            result = TOOL_HANDLERS[name](args)
            print(f"  {DIM}  = {result[:150]}{RESET}")
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        print(f"  {DIM}→ Looping back to call model again...{RESET}")
