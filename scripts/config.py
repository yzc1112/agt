#!/usr/bin/env python3
"""
Shared configuration for all step scripts.
Loads API credentials from .env and creates an OpenAI-compatible client.

Setup:
  1. cp config.example.env .env
  2. Fill in your API_KEY, BASE_URL, and MODEL
  3. All step scripts will auto-load this file

Supports any OpenAI-compatible API (MiniMax, OpenAI, Ollama, etc.)
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Find .env relative to this file's directory (works regardless of cwd)
_script_dir = Path(__file__).parent.resolve()
load_dotenv(_script_dir / ".env")

# ── API Credentials ─────────────────────────────────────────────────────────
API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://api.minimax.chat/v1")
MODEL = os.getenv("MODEL", "MiniMax-M2.7")

# ── Create client ─────────────────────────────────────────────────────────────
from openai import OpenAI

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

__all__ = ["client", "MODEL", "API_KEY", "BASE_URL"]
