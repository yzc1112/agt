# Building an AI Agent — Step by Step

A hands-on workshop for understanding how AI agents work under the hood. From a single LLM call to a full autonomous agent — every concept, every line of code, from scratch.

**Author: Zichao Yang**

---

## Quick Start (Choose One)

### Option 1 — View Static Slides (Easiest, No Setup)

Just want to view the slides? No Python needed. All code examples and explanations are there — but the live demo terminals will NOT execute real code.

```bash
# Double-click to open in browser:
demo-server/static/index.html

# Or drag the file into any browser window
```

---

### Option 2 — Full Slides with Live Demos

Get the interactive presentation with live Python demos running in your browser. Requires more setup.

**Before you start — add your API key:**

```bash
# 1. Go to scripts/ and create your .env file
cd scripts
cp config.example.env .env
# 2. Edit .env — fill in API_KEY, BASE_URL, and MODEL
```

**Then run the server:**

```bash
# 3. Create venv and install
cd demo-server
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Start the server (use venv Python, NOT system python3)
./venv/bin/python3 server.py

# 5. Open in browser
open http://localhost:8000
```

Navigate with arrow keys or click the dots. The live demos will execute real Python in your browser.

---

### Option 3 — Run the Python Scripts Directly

Run the agent scripts in your terminal. Each step is self-contained.

**Before you start:**

```bash
# 1. Go to scripts/ and create your .env file
cd scripts
cp config.example.env .env
# 2. Edit .env — fill in API_KEY, BASE_URL, and MODEL
```

**Then run any step:**

```bash
# 3. Create venv and install deps
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Run any step
python3 step01_hello_llm.py
python3 step04_agent_loop.py
# ...etc
```

---

## Project Structure

```
agt/
├── demo-server/           # Slides + live demo server (Option 2)
│   ├── server.py          # WebSocket + FastAPI server
│   ├── requirements.txt   # Python deps
│   └── static/
│       ├── index.html    # Slide deck (also opens standalone, Option 1)
│       ├── js/           # Slide logic, terminal manager
│       └── css/          # Styles
│
├── scripts/              # Python step scripts (Option 3)
│   ├── config.py              # Shared API config
│   ├── config.example.env     # Template — copy to .env and fill in key
│   ├── step01_hello_llm.py   # One LLM call
│   ├── step02_chat_loop.py    # + message history
│   ├── step03_tool_use.py     # + tool calls
│   ├── step04_agent_loop.py  # + inner loop (autonomy)
│   ├── step05_planning.py     # + explicit todo state
│   ├── step06_memory.py       # + file-based memory
│   ├── step07_subagent.py     # + subagents
│   ├── step08_team.py         # + multi-agent teams
│   └── step09_final_agent.py  # complete agent
```

---

## The 9 Steps

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
| 09 | `step09_final_agent.py` | Complete agent with all concepts |

---

## API Configuration

Edit `scripts/.env` (copy from `config.example.env` if missing). Only 3 values needed:

```env
API_KEY=your_api_key_here
BASE_URL=https://api.minimax.chat/v1
MODEL=MiniMax-M2.7
```

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_KEY` | Yes | — | Your API key |
| `BASE_URL` | No | `https://api.minimax.chat/v1` | API endpoint |
| `MODEL` | No | `MiniMax-M2.7` | Model name |

**Examples:**
```env
# MiniMax
API_KEY=sk-xxx
BASE_URL=https://api.minimax.chat/v1
MODEL=MiniMax-M2.7

# OpenAI
API_KEY=sk-xxx
BASE_URL=https://api.openai.com/v1
MODEL=gpt-4o

# Ollama (local)
API_KEY=ollama
BASE_URL=http://localhost:11434/v1
MODEL=llama3
```

---

## Requirements

- Python 3.8+
- API key: [MiniMax](https://api.minimax.chat/) · [OpenAI](https://platform.openai.com/) · or any OpenAI-compatible provider

---

## License

MIT
