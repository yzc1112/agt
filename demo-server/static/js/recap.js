// Recap slide: animated build-up from simple LLM call to full agent

const RECAP_STEPS = [
  {
    title: 'Step 1 — The Simplest Agent',
    code: `<span class="cmt"># Step 1: The simplest agent</span>
<span class="cmt"># One LLM call, nothing else</span>
response = llm.<span class="fn">generate</span>(<span class="fn">input</span>(<span class="str">"You: "</span>))`,
    desc: 'Hello LLM: A single call. Prompt in, response out. No memory, no tools, no loop.'
  },
  {
    title: 'Step 2 — Add Chat Loop + Message History',
    code: `<span class="cmt"># Step 2: Add a chat loop + message history</span>
<span class="cmt"># LLM now remembers within a session</span>
messages = []
<span class="kw">while</span> <span class="num">True</span>:
    messages.<span class="fn">append</span>(<span class="fn">input</span>(<span class="str">"You: "</span>))

    response = llm.<span class="fn">generate</span>(messages)
    messages.<span class="fn">append</span>(response)`,
    desc: 'Chat Loop: messages[] accumulates. Turn 2 knows what Turn 1 said. "Who am I?" → "Zichao"'
  },
  {
    title: 'Step 3 — Give the Agent Tools (Hands)',
    code: `<span class="cmt"># Step 3: Give the agent tools (hands)</span>
messages = []
tools = [<span class="str">"run_bash"</span>]

<span class="kw">while</span> <span class="num">True</span>:
    messages.<span class="fn">append</span>(<span class="fn">input</span>(<span class="str">"You: "</span>))
    response = llm.<span class="fn">generate</span>(messages, tools=tools)

    <span class="kw">if</span> response.tool_calls:
        messages.<span class="fn">append</span>(<span class="fn">execute</span>(response.tool_calls))
        response = llm.<span class="fn">generate</span>(messages)  <span class="cmt"># 2nd call with result</span>

    messages.<span class="fn">append</span>(response)`,
    desc: 'Tool Use: LLM calls run_bash("ls") → result → 2nd LLM call. Agent has "hands" now.'
  },
  {
    title: 'Step 4 — Agent Loop (Nested Autonomy)',
    code: `<span class="cmt"># Step 4: Agent loop (nested autonomy)</span>
messages = []
tools = [<span class="str">"run_bash"</span>]

<span class="kw">while</span> <span class="num">True</span>:      <span class="cmt"># Outer: human turns</span>
    messages.<span class="fn">append</span>(<span class="fn">input</span>(<span class="str">"You: "</span>))

    <span class="kw">while</span> <span class="num">True</span>:    <span class="cmt"># Inner: agent autonomy</span>
        response = llm.<span class="fn">generate</span>(messages, tools=tools)
        messages.<span class="fn">append</span>(response)

        <span class="kw">if not</span> response.tool_calls: <span class="kw">break</span>  <span class="cmt"># Done thinking</span>

        messages.<span class="fn">append</span>(<span class="fn">execute</span>(response.tool_calls))`,
    desc: 'Agent Loop: Inner loop keeps calling tools until LLM says "I\'m done." Outer loop handles human turns.'
  },
  {
    title: 'Step 5 — Explicit Planning State',
    code: `<span class="cmt"># Step 5: Explicit planning state</span>
messages = []
todos = []  <span class="cmt"># Planning: The agent's active roadmap</span>
tools = [<span class="str">"run_bash"</span>, <span class="str">"update_todo"</span>]

<span class="kw">while</span> <span class="num">True</span>:
    messages.<span class="fn">append</span>(<span class="fn">input</span>(<span class="str">"You: "</span>))

    <span class="kw">while</span> <span class="num">True</span>:
        context = messages + [<span class="str">f"Current Plan: {todos}"</span>]
        response = llm.<span class="fn">generate</span>(context, tools=tools)
        messages.<span class="fn">append</span>(response)

        <span class="kw">if not</span> response.tool_calls: <span class="kw">break</span>

        result = <span class="fn">execute</span>(response.tool_calls)
        messages.<span class="fn">append</span>(result)

        todos = <span class="fn">update_todos</span>(todos, result)`,
    desc: 'Planning: Agent sees its own todo state. "update_todo" tool lets LLM modify the roadmap progressively.'
  },
  {
    title: 'Step 6 — Add File-Based Memory (Persistence)',
    code: `<span class="cmt"># Step 6: Add file-based memory (persistence)</span>
messages = []
todos = []
memory = <span class="fn">read_file</span>(<span class="str">"memory.txt"</span>)  <span class="cmt"># Load long-term context</span>
tools = [<span class="str">"run_bash"</span>, <span class="str">"update_todo"</span>, <span class="str">"save_file"</span>]

<span class="kw">while</span> <span class="num">True</span>:
    messages.<span class="fn">append</span>(<span class="fn">input</span>(<span class="str">"You: "</span>))

    <span class="kw">while</span> <span class="num">True</span>:
        context = messages + [<span class="str">f"Todos: {todos}"</span>, <span class="str">f"Memory: {memory}"</span>]
        response = llm.<span class="fn">generate</span>(context, tools=tools)
        messages.<span class="fn">append</span>(response)

        <span class="kw">if not</span> response.tool_calls: <span class="kw">break</span>

        result = <span class="fn">execute</span>(response.tool_calls)
        messages.<span class="fn">append</span>(result)

        todos = <span class="fn">update_todos</span>(todos, result)
        <span class="fn">save_file</span>(<span class="str">"memory.txt"</span>, todos)  <span class="cmt"># Persist to disk</span>`,
    desc: 'Memory: State survives program restart. read_file at start, save_file after each update. Memory persists across sessions.'
  },
];

let recapIndex = 0;
let isAnimating = false;

function recapStep(dir) {
  if (isAnimating) return;
  const next = recapIndex + dir;
  if (next < 0 || next >= RECAP_STEPS.length) return;

  isAnimating = true;
  recapIndex = next;

  const titleEl = document.getElementById('recap-step-title');
  const codeEl = document.getElementById('recap-code');
  const descEl = document.getElementById('recap-desc');

  // Build-on effect: lines cascade down, new content "builds in"
  // First, fade title up and shrink code slightly
  titleEl.style.opacity = '0';
  titleEl.style.transform = 'translateY(-12px)';
  codeEl.style.opacity = '0';
  codeEl.style.transform = 'translateY(-8px) scale(0.98)';
  descEl.style.opacity = '0';

  setTimeout(() => {
    // Update content
    const step = RECAP_STEPS[recapIndex];
    titleEl.innerHTML = step.title;
    codeEl.innerHTML = step.code;
    descEl.innerHTML = `<span style="color: var(--accent-cyan);">${step.desc}</span>`;

    // Update label
    document.getElementById('recap-step-label').textContent = `${recapIndex + 1} / 6`;

    // Update buttons
    document.getElementById('recap-prev').style.opacity = recapIndex === 0 ? '0.3' : '1';
    document.getElementById('recap-next').style.opacity = recapIndex === RECAP_STEPS.length - 1 ? '0.3' : '1';

    // Title slides in from top
    titleEl.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
    titleEl.style.opacity = '1';
    titleEl.style.transform = 'translateY(0)';

    // Code "builds in" from top with cascading lines
    // First position off-screen above
    codeEl.style.transform = 'translateY(-20px) scale(0.97)';
    codeEl.style.opacity = '0';

    setTimeout(() => {
      // Then animate to final position with spring-like effect
      codeEl.style.transition = 'opacity 0.4s ease, transform 0.5s cubic-bezier(0.34, 1.2, 0.64, 1)';
      codeEl.style.opacity = '1';
      codeEl.style.transform = 'translateY(0) scale(1)';

      setTimeout(() => {
        // Description fades in last
        descEl.style.transition = 'opacity 0.35s ease';
        descEl.style.opacity = '1';
        isAnimating = false;
      }, 200);
    }, 100);
  }, 280);
}

function updateRecap() {
  const step = RECAP_STEPS[recapIndex];
  const titleEl = document.getElementById('recap-step-title');
  const codeEl = document.getElementById('recap-code');
  const descEl = document.getElementById('recap-desc');

  titleEl.innerHTML = step.title;
  codeEl.innerHTML = step.code;
  descEl.innerHTML = `<span style="color: var(--accent-cyan);">${step.desc}</span>`;
  document.getElementById('recap-step-label').textContent = `${recapIndex + 1} / 6`;
}

// Init on page load
document.addEventListener('DOMContentLoaded', () => {
  updateRecap();
});
