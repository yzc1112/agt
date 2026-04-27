#!/usr/bin/env python3
"""
Step 2: The Conversation Loop
A while loop turns a single LLM call into an interactive chatbot.
What's new: while True loop, message history accumulation.
Key insight: messages[] grows with every turn — the model sees the full history.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from display import print_thinking, BLUE, GREEN, DIM, RESET

load_dotenv()

client = OpenAI(api_key=os.getenv("MINIMAX_API_KEY"), base_url="https://api.minimax.chat/v1")
MODEL = "MiniMax-M2.7"

messages = [
    {"role": "system", "content": "You are a helpful assistant. Be concise."},
]

print("=" * 50)
print("Step 2: The Conversation Loop")
print('Sample: "Hi. My name is Zichao." -> "What is my name?"')
print("  (2nd prompt tests whether the model remembers context)")
print("=" * 50)

turn = 0
# User Turns
while True: 
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    turn += 1
    messages.append({"role": "user", "content": user_input})

    # ── REQUEST: show everything we're about to send ─────────────────────────────
    print(f"\n{BLUE}═══ Turn {turn} ════════════════════════════════{RESET}")
    print(f"{BLUE}─── REQUEST (what we send to the model) ────{RESET}")
    print(f"  model: {MODEL}   messages in history: {len(messages)}")
    for i, m in enumerate(messages):
        role = m["role"]
        content = str(m.get("content") or "")[:80].replace("\n", " ")
        marker = " ← NEW" if i == len(messages) - 1 and role == "user" else ""
        print(f"  [{i}] {role:10s}: \"{content}...\"{marker}")
    print(f"{BLUE}─────────────────────────────────────────────{RESET}")

    # ── Call the model ──────────────────────────────────────────────────────────
    response = client.chat.completions.create(model=MODEL, messages=messages)
    choice = response.choices[0]
    assistant_message = choice.message.content

    # ── RESPONSE: show what the model returned ──────────────────────────────────
    print(f"{GREEN}─── RESPONSE (what the model returns) ────{RESET}")
    print(f"  finish_reason: {choice.finish_reason!r}")
    print(f"  content:       \"{(assistant_message or '')[:120]}\"")
    print(f"  usage:         prompt={response.usage.prompt_tokens}"
          f"  completion={response.usage.completion_tokens}"
          f"  total={response.usage.total_tokens}")
    print(f"{GREEN}─────────────────────────────────────────────{RESET}")

    messages.append({"role": "assistant", "content": assistant_message})
    print_thinking(assistant_message)
