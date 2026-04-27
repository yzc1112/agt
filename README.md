# Building an AI Agent — Step by Step

A hands-on workshop for understanding how AI agents work under the hood. From a single LLM call to a full autonomous agent — every concept, every line of code, from scratch.

---

## Quick Start (Choose One)

### Option 1 — Full Slides with Live Demos (Recommended for Presentations)

Get the interactive presentation with live Python demos running in your browser.

```bash
# 1. Clone and enter
git clone https://github.com/yzc1112/agt.git
cd agt

# 2. Create venv and install
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r demo-server/requirements.txt

# 3. Start the server
cd demo-server
python3 server.py

# 4. Open in browser
open http://localhost:8000
```

That's it. Navigate with arrow keys or click the dots.

---

### Option 2 — Static Slides Only (No Setup, No Demos)

Just want to view the slides? No Python needed.

```bash
# Just open this file in any browser:
open demo-server/static/index.html

# Or deploy to Vercel (free) for a shareable URL:
npx vercel deploy ./demo-server/static --prod
```

The slides work standalone — no server required. The live demo terminals won't execute code, but all the explanations and code examples are there.

---

### Option 3 — Run the Python Scripts Directly (No Slides)

Just want to run the agent scripts in your terminal? Each step is self-contained.

```bash
# 1. Clone
git clone https://github.com/yzc1112/agt.git
cd agt/scripts

# 2. Install deps
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Set your API key (MiniMax or OpenAI)
export MINIMAX_API_KEY=your_key_here

# 4. Run any step
python3 step01_hello_llm.py
python3 step04_agent_loop.py
# ...etc
```

---

## Project Structure

```
agt/
├── demo-server/           # Interactive presentation (Option 1)
│   ├── server.py          # WebSocket + FastAPI server
│   ├── requirements.txt   # Python deps for the server
│   └── static/
│       ├── index.html    # Slide deck (also works standalone, Option 2)
│       ├── js/           # Slide logic, terminal manager
│       └── css/          # Styles
│
├── scripts/              # Python step scripts (Option 3)
│   ├── step01_hello_llm.py      # One LLM call
│   ├── step02_chat_loop.py       # + message history
│   ├── step03_tool_use.py        # + tool calls
│   ├── step04_agent_loop.py      # + inner loop (autonomy)
│   ├── step05_planning.py         # + explicit todo state
│   ├── step06_memory.py          # + file-based memory
│   ├── step07_subagent.py        # + subagents
│   ├── step08_team.py           # + multi-agent teams
│   └── step09_final_agent.py    # complete agent
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

## Requirements

- Python 3.8+
- API key: [MiniMax API](https://api.minimax.chat/) (or modify scripts to use OpenAI/Anthropic)

---

## License

MIT
