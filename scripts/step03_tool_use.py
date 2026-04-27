#!/usr/bin/env python3
"""
Step 3: Giving the LLM Hands
Define a tool (bash), let the LLM call it, return the result.
What's new: tool definitions, tool_calls detection, executing tools.
"""
import json
import os
import subprocess
from config import client, MODEL
from display import print_thinking, BLUE, GREEN, YELLOW, DIM, RESET


def show_request(messages, tools=None):
    for i, m in enumerate(messages):
        role = m["role"] if isinstance(m, dict) else m.role
        content = str(m.get("content") or "") if isinstance(m, dict) else str(m.content or "")
        preview = content[:80].replace("\n", " ")
        print(f"  [{i}] {role:10s}: \"{preview}{'...' if len(content) > 80 else ''}\"")
    if tools:
        print(f"  tools available: {[t['function']['name'] for t in tools]}")


def show_response(choice):
    msg = choice.message
    print(f"  finish_reason : {choice.finish_reason!r}")
    if msg.tool_calls:
        print(f"  content       : null  (no text answer yet)")
        print(f"  tool_calls    :")
        for i, tc in enumerate(msg.tool_calls):
            print(f"    [{i}] id        = {tc.id}")
            print(f"        function  = {tc.function.name}")
            print(f"        arguments = {tc.function.arguments}")
    else:
        print(f"  content       : \"{(msg.content or '')[:200]}\"")


def show_append(label, msg_dict):
    compact = json.dumps(msg_dict, indent=2, ensure_ascii=False)
    if len(compact) > 400:
        compact = compact[:400] + "\n  ..."
    print(f"{YELLOW}─── APPEND TO messages[] ({label}) ────────{RESET}")
    print(f"  {compact}")


tools = [
    {
        "type": "function",
        "function": {
            "name": "run_bash",
            "description": "Run a bash command and return its output.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string", "description": "The bash command to run"}},
                "required": ["command"],
            },
        },
    }
]


def run_bash(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
    return (result.stdout + result.stderr).strip() or "(no output)"


messages = [
    {"role": "system", "content": "You are a helpful assistant with access to a bash tool. Use it to answer questions."},
]

print("=" * 50)
print("Step 3: Tool Use — Giving the LLM Hands")
print('Sample: "What files are in the current directory?"')
print("  1 request + 1 tool call + 1 response = 1 complete round")
print("=" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    messages.append({"role": "user", "content": user_input})

    # ── REQUEST: ask the model ────────────────────────────────────────────────
    print(f"\n{BLUE}─── REQUEST ──────────────────────────────────────{RESET}")
    show_request(messages, tools)
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    choice = response.choices[0]
    msg = choice.message
    print(f"\n{BLUE}─── RESPONSE (tool result) ─────────{RESET}")
    show_response(choice)
    messages.append(msg)

    # ── If model wants a tool, execute it ───────────────────────────────────
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            print(f"\n  >>> Executing: run_bash({args['command']!r})")
            result = run_bash(args["command"])
            print(f"  >>> Result: {result[:300]}")

            tool_result = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            show_append("tool result", tool_result)
            messages.append(tool_result)

        # ── RESPONSE: model reads tool result and answers ───────────────────
        print(f"\n{BLUE}─── RESPONSE (model reads tool result) ─────────{RESET}")
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        choice = response.choices[0]
        msg = choice.message
        show_response(choice)
        messages.append(msg)

    print_thinking(msg.content)
