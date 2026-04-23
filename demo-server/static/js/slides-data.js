// Slide definitions for the AI Agent presentation
// Each slide has: id, stepLabel, title, content type, and slide-specific data

const SLIDES = [
  // Slide 00: Title
  { id: 'title', stepNum: '00', stepLabel: null, title: 'Building an AI Agent<br>Step by Step', type: 'title' },

  // Slide 01: Outline
  { id: 'outline', stepNum: '01', stepLabel: 'Overview', title: 'What We Will Walk Through', type: 'outline' },

  // Slide 02: What is an Agent?
  { id: 'what-is-agent', stepNum: '02', stepLabel: null, title: 'From Chatbots to Workers', type: 'what-is-agent' },

  // Slide 03: Step 01 — Hello LLM
  { id: 'step-01', stepNum: '03', stepLabel: 'Step 01', title: 'Hello, LLM', type: 'code-with-flow' },
  // Slide 03b: Demo
  { id: 'demo-01', stepNum: '03b', stepLabel: 'Live Demo', title: 'Hello, LLM — Real Execution', type: 'demo', script: 'step01_hello_llm.py' },

  // Slide 04: Step 02 — Chat Loop
  { id: 'step-02', stepNum: '04', stepLabel: 'Step 02', title: 'Chat Loop — Memory Through History', type: 'code-with-flow' },
  // Slide 04b: Demo
  { id: 'demo-02', stepNum: '04b', stepLabel: 'Live Demo', title: 'Chat Loop — Multi-Turn Memory', type: 'demo', script: 'step02_chat_loop.py' },

  // Slide 05: Step 03 — Tool Use
  { id: 'step-03', stepNum: '05', stepLabel: 'Step 03', title: 'Tool Use — Giving the Agent Hands', type: 'code-with-flow' },
  // Slide 05b: Demo
  { id: 'demo-03', stepNum: '05b', stepLabel: 'Live Demo', title: 'Tool Use — Real Python Execution', type: 'demo', script: 'step03_tool_use.py' },

  // Slide 06: Step 04 — Agent Loop
  { id: 'step-04', stepNum: '06', stepLabel: 'Step 04', title: 'Agent Loop — Autonomy Through Nested Loops', type: 'code-static' },
  // Slide 06b: Demo — Step 04 Agent Loop
  { id: 'demo-04', stepNum: '06b', stepLabel: 'Live Demo', title: 'Agent Loop — Nested Autonomy', type: 'demo', script: 'step04_agent_loop.py' },

  // Slide 07: Step 05 & 06 — Planning + Memory
  { id: 'step-05-06', stepNum: '07', stepLabel: 'Step 05 & 06', title: 'Planning + Memory — Stateful Agents', type: 'code-static' },
  // Slide 07b: Demo — Step 05 Planning
  { id: 'demo-05', stepNum: '07b', stepLabel: 'Live Demo', title: 'Planning — Todo State Management', type: 'demo', script: 'step05_planning.py' },
  // Slide 07c: Demo — Step 06 Memory
  { id: 'demo-06', stepNum: '07c', stepLabel: 'Live Demo', title: 'Memory — File-Based Persistence', type: 'demo', script: 'step06_memory.py' },

  // Slide 08: Step 07 & 08 — Subagents & Teams
  { id: 'step-07-08', stepNum: '08', stepLabel: 'Step 07 & 08', title: 'Subagents & Teams — Scaling Autonomy', type: 'code-static' },

  // Slide 09: Recap — Build up to current agent
  { id: 'recap', stepNum: '09', stepLabel: 'Recap', title: 'From Simple Call to Full Agent', type: 'recap' },

  // Slide 10: The Production Gap
  { id: 'production-gap', stepNum: '10', stepLabel: 'The Production Gap', title: 'The Reality Check', type: 'production-gap' },

  // Slide 11: Takeaway
  { id: 'takeaway', stepNum: '11', stepLabel: 'Final Thoughts', title: null, type: 'takeaway' },
];

// Flow step data for slides with interactive steppers
const FLOW_DATA = {
  'step-01': {
    codeLines: [
      { id: 'flow01-line-0', html: 'user_input = <span class="fn">input</span>(<span class="str">"You: "</span>)' },
      { id: 'flow01-line-1', html: 'response = llm.<span class="fn">generate</span>(user_input)', dim: true },
      { id: 'flow01-line-2', html: '<span class="fn">print</span>(response)', dim: true },
    ],
    steps: [
      { lines: [0], card: 1 },
      { lines: [1, 2], card: 2 },
    ],
    cards: [
      {
        id: 'flow01-card-1',
        label: '① USER INPUT',
        color: 'cyan',
        content: [
          { style: 'blue', text: '"Hello, I am Zichao"' },
          { style: 'gray', text: 'Single prompt in', small: true },
        ]
      },
      {
        id: 'flow01-card-2',
        label: '② LLM OUTPUT',
        color: 'cyan',
        content: [
          { style: 'blue', text: '"Hello Zichao! Nice to meet you."' },
          { style: 'gray', text: 'Done — program exits', small: true },
        ]
      },
    ],
    comparison: [
      { label: 'No Memory', color: 'cyan', text: 'Each call is isolated', code: '"Who am I?" → "I don\'t know"' },
      { label: 'With Memory', color: 'magenta', text: 'Messages keep history', codeMultiline: ['messages:', '  "I am Zichao" ← user', '  "Hello Zichao" ← assistant'] },
    ],
  },

  'step-02': {
    codeLines: [
      { id: 'flow02-line-0', html: 'messages = []' },
      { id: 'flow02-line-1', html: '<span class="kw">while</span> <span class="num">True</span>:' },
      { id: 'flow02-line-2', html: '    user_input = <span class="fn">input</span>(<span class="str">"You: "</span>)' },
      { id: 'flow02-line-3', html: '    messages.<span class="fn">append</span>(user_input)' },
      { id: 'flow02-line-4', html: '    response = llm.<span class="fn">generate</span>(messages)', dim: true },
      { id: 'flow02-line-5', html: '    messages.<span class="fn">append</span>(response)', dim: true },
      { id: 'flow02-line-6', html: '    <span class="fn">print</span>(<span class="str">"Agent:"</span>, response.text)', dim: true },
    ],
    steps: [
      { lines: [0, 1, 2, 3, 4], card: 1 },
      { lines: [1, 2, 3, 4, 5, 6], card: 2 },
    ],
    cards: [
      {
        id: 'flow02-card-1',
        label: 'Step 1',
        color: 'cyan',
        content: [
          { style: 'gray', text: 'SENT:' },
          { style: 'teal', text: '{ role: "user", content: "Hi" }' },
          { style: 'gray', text: 'RECEIVED:' },
          { style: 'blue', text: '{ role: "assistant", content: "Hello!" }' },
        ]
      },
      {
        id: 'flow02-card-2',
        label: 'Step 2 (+1 turn)',
        color: 'blue',
        content: [
          { style: 'gray', text: 'SENT (full history):' },
          { style: 'purple', text: 'messages: [' },
          { style: 'teal', text: '  { role: "user", content: "Hi" },        ← Turn 1' },
          { style: 'teal', text: '  { role: "assistant", content: "Hello!" }, ← Turn 1' },
          { style: 'teal', text: '  { role: "user", content: "What is my name?" } ← Turn 2 (NEW)' },
          { style: 'purple', text: ']' },
          { style: 'gray', text: 'RECEIVED:' },
          { style: 'blue', text: '{ role: "assistant", content: "You are Zichao" }' },
        ]
      },
    ],
    comparison: [
      { label: 'Without Loop (Step 01)', color: 'cyan', text: 'LLM is stateless — no memory', code: '"Hi" → "Hello, who?"' },
      { label: 'With Loop (Step 02)', color: 'magenta', text: 'messages[] grows with turns', code: 'Turn 1: "I am Zichao"\nTurn 2: "What is my name?" → "Zichao"' },
    ],
  },

  'step-03': {
    codeLines: [
      { id: 'flow-line-0', html: '<span class="kw">def</span> <span class="fn">run_bash</span>(command): ...' },
      { id: 'flow-line-1', html: 'tools = [<span class="str">"run_bash"</span>]' },
      { id: 'flow-line-2', html: 'system_message = {<span class="str">"role"</span>: <span class="str">"system"</span>, <span class="str">"content"</span>: <span class="str">"You have access to: run_bash"</span>}' },
      { id: 'flow-line-3', html: 'user_message = {<span class="str">"role"</span>: <span class="str">"user"</span>, <span class="str">"content"</span>: user_input}' },
      { id: 'flow-line-4', html: 'messages = [system_message, user_message]' },
      { id: 'flow-line-5', html: 'response = llm.<span class="fn">generate</span>(messages, tools=tools)', dim: true },
      { id: 'flow-line-6', html: '<span class="kw">if</span> response.tool_calls:', dim: true },
      { id: 'flow-line-7', html: '    result = <span class="fn">run_bash</span>(...)', dim: true },
      { id: 'flow-line-8', html: 'messages.append({role:"tool", content: result})', dim: true },
      { id: 'flow-line-9', html: 'response = llm.<span class="fn">generate</span>(messages)', dim: true },
      { id: 'flow-line-10', html: '<span class="kw">print</span>(<span class="str">"Agent:"</span>, response.text)', dim: true },
    ],
    steps: [
      { lines: [0, 1, 2, 3, 4, 5], card: 1 },
      { lines: [5, 6, 7], card: 2 },
      { lines: [7, 8, 9, 10], card: 3 },
    ],
    cards: [
      {
        id: 'flow-card-1',
        label: '① REQUEST → LLM',
        color: 'cyan',
        content: [
          { style: 'purple', text: 'messages: [' },
          { style: 'teal', text: 'system: "You have access to: run_bash"' },
          { style: 'teal', text: 'user: "list files"' },
          { style: 'purple', text: ']' },
          { style: 'gray', text: 'tools: [<span style="color:#ce9178">"run_bash"</span>]' },
        ]
      },
      {
        id: 'flow-card-2',
        label: '② TOOL CALL',
        color: 'magenta',
        content: [
          { style: 'purple', text: 'tool_calls: [' },
          { style: 'red', text: 'name: <span style="color:#a5d6ff">"run_bash"</span>,' },
          { style: 'red', text: 'arguments:' },
          { style: 'blue', text: '  {"command": "ls -la"}' },
          { style: 'purple', text: ']' },
          { style: 'green', text: '→ execute("ls -la")' },
        ]
      },
      {
        id: 'flow-card-3',
        label: '③ FINAL RESPONSE',
        color: 'cyan',
        content: [
          { style: 'blue', text: 'Agent: "Here are the files:' },
          { style: 'blue', text: '  agt/  step01_hello_llm.py' },
          { style: 'blue', text: '  step02_chat_loop.py ..."' },
        ]
      },
    ],
    comparison: [
      { label: 'Without Tools', color: 'cyan', text: 'LLM returns plain text', code: '"Here\'s what I found..."' },
      { label: 'With Tools', color: 'magenta', text: 'LLM returns tool_calls', codeMultiline: ['tool_calls: [', '  name: "run_bash"', ']'] },
    ],
  },
};