#!/usr/bin/env python3
"""
Step 1: Hello, LLM
Connect to an LLM and get a response. That's it.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from display import print_thinking, BLUE, GREEN, DIM, RESET

load_dotenv()

client = OpenAI(
    api_key=os.getenv("MINIMAX_API_KEY"),
    base_url="https://api.minimax.chat/v1",
)
MODEL = "MiniMax-M2.7"

print("=" * 50)
print("Step 1: Hello, LLM")
print('Sample: "Hello, I am Zichao"')
print("=" * 50)

user_input = input("\nYou: ")

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": user_input}],
)

choice = response.choices[0]

# --- Educational: show the raw response object ---
print(f"\n{GREEN}─── Raw Response Object ───────────────────{RESET}")
print(f"  model:         {response.model}")
print(f"  finish_reason: {choice.finish_reason}")
print(f"  role:          {choice.message.role}")
print(f"  usage:         prompt={response.usage.prompt_tokens}"
      f"  completion={response.usage.completion_tokens}"
      f"  total={response.usage.total_tokens}")
print(f"{GREEN}───────────────────────────────────────────{RESET}")

print_thinking(choice.message.content)
