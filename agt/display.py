"""
Shared display helpers for the step-by-step agent workshop.
Keeps all educational output formatting in one place.
"""
import re

# ANSI colors
BLUE  = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
DIM   = "\033[2m"
CYAN  = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

BOX_WIDTH = 50


def print_thinking(content, label="Assistant"):
    """Strip <think>...</think> and display with thinking separated from answer."""
    if not content:
        return
    if "</think>" in content:
        thoughts = re.findall(r"<think>(.*?)</think>", content, re.DOTALL)
        answer = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        print(f"\n{BLUE}┌─ {label} ─{'─' * (BOX_WIDTH - len(label) - 4)}{RESET}")
        for thought in thoughts:
            print(f"  {DIM}[thinking] {thought.strip()}{RESET}")
        if answer:
            print(f"  {answer}")
        print(f"{BLUE}└{'─' * (BOX_WIDTH - 2)}{RESET}")
    else:
        print(f"\n{BLUE}┌─ {label} ─{'─' * (BOX_WIDTH - len(label) - 4)}{RESET}")
        print(f"  {content}")
        print(f"{BLUE}└{'─' * (BOX_WIDTH - 2)}{RESET}")
