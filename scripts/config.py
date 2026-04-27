#!/usr/bin/env python3
"""
Shared configuration for all step scripts.
Loads API credentials from .env and creates an OpenAI-compatible client.

Setup:
  1. cp config.example.env .env
  2. Fill in your API key and provider
  3. All step scripts will auto-load this file

Providers supported:
  - MiniMax (default): set MINIMAX_API_KEY
  - OpenAI: set OPENAI_API_KEY
  - Any OpenAI-compatible API: set API_KEY + BASE_URL + MODEL
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Find .env relative to this file's directory (works regardless of cwd)
_script_dir = Path(__file__).parent.resolve()
load_dotenv(_script_dir / ".env")

# ── Provider selection ────────────────────────────────────────────────────────
_provider = os.getenv("PROVIDER", "minimax").lower()

if _provider == "openai":
    _api_key  = os.getenv("OPENAI_API_KEY")
    _base_url = "https://api.openai.com/v1"
    _model    = os.getenv("OPENAI_MODEL", "gpt-4o")
else:
    _api_key  = os.getenv("MINIMAX_API_KEY")
    _base_url = os.getenv("BASE_URL", "https://api.minimax.chat/v1")
    _model    = os.getenv("MODEL", "MiniMax-M2.7")

# ── Create client ─────────────────────────────────────────────────────────────
from openai import OpenAI

client = OpenAI(api_key=_api_key, base_url=_base_url)
MODEL  = _model

__all__ = ["client", "MODEL"]
