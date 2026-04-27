# Building an AI Agent — Step by Step

A hands-on workshop for understanding how AI agents work under the hood. From a single LLM call to a full autonomous agent — every concept, every line of code, from scratch.

## What's Here

```
agt/                    # Step-by-step Python scripts
  step01_hello_llm.py   # Simplest possible LLM call
  step02_chat_loop.py   # Add message history (session memory)
  step03_tool_use.py    # Give the agent tools (run_bash, read/write files)
  step04_agent_loop.py  # Agent autonomy — inner loop until done
  step05_planning.py    # Explicit todo/planning state
  step06_memory.py      # File-based long-term memory
  step07_subagent.py    # Split into specialized subagents
  step08_team.py        # Multi-agent coordination

demo-server/            # Live presentation server
  server.py             # FastAPI WebSocket server
  static/
    index.html          # Interactive slide deck
    js/                 # Slide logic, flow steppers, terminal manager
    css/                # Presentation styles
```

## Quick Start

### Run the Presentation

```bash
cd demo-server
pip install fastapi uvicorn websockets
python3 server.py
# Open http://localhost:8000
```

The presentation includes live demos that run each step script directly in the browser via WebSocket + xterm.js.

### Run a Script Manually

```bash
cd agt
pip install python-dotenv openai

# Set your API key
export MINIMAX_API_KEY=your_key_here

# Run any step
python3 step01_hello_llm.py
```

## The 8 Steps

| Step | File | What You Learn |
|------|------|----------------|
| 01 | `step01_hello_llm.py` | One prompt in, one response out |
| 02 | `step02_chat_loop.py` | Message history for session memory |
| 03 | `step03_tool_use.py` | Tool calls — give the agent "hands" |
| 04 | `step04_agent_loop.py` | Inner loop: agent keeps acting until done |
| 05 | `step05_planning.py` | Explicit todo state the agent can update |
| 06 | `step06_memory.py` | File-based persistence across sessions |
| 07 | `step07_subagent.py` | Split into specialized subagents |
| 08 | `step08_team.py` | Multi-agent orchestration |

## Slides

The `demo-server/` folder is a self-contained HTML presentation with:

- Animated slide transitions and flow steppers
- Live Python execution in-browser via WebSocket
- Interactive recap showing the build-up from simple call to full agent

## Requirements

- Python 3.8+
- [MiniMax API](https://api.minimax.chat/) (or modify to use OpenAI/Anthropic)
- `pip install python-dotenv openai` for the scripts

## License

MIT
