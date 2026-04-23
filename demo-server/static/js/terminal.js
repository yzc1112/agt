// Terminal manager — shared code for all demo slides
// Handles WebSocket connection, xterm.js setup, line buffer for backspace/echo

class TerminalManager {
  constructor(containerId, scriptName, filenameId, codeDisplayId) {
    this.containerId = containerId;
    this.scriptName = scriptName;
    this.filenameId = filenameId;
    this.codeDisplayId = codeDisplayId;
    this.term = null;
    this.ws = null;
    this.fitAddon = null;
    this.lineBuf = '';
    this.started = false;
  }

  async loadCode() {
    try {
      const resp = await fetch('/step/' + this.scriptName);
      if (!resp.ok) throw new Error('not found');
      const code = await resp.text();
      document.getElementById(this.filenameId).textContent = this.scriptName;
      const pre = document.getElementById(this.codeDisplayId);
      pre.innerHTML = Prism.highlight(code, Prism.languages.python, 'python');
    } catch (e) {
      document.getElementById(this.codeDisplayId).textContent = 'Error loading code: ' + e.message;
    }
  }

  start() {
    if (this.started) return;
    this.started = true;

    if (this.term) this.term.dispose();
    if (this.ws) this.ws.close();

    this.term = new Terminal({
      cursorBlink: true,
      fontFamily: "'Fira Code', 'Cascadia Code', 'JetBrains Mono', Menlo, monospace",
      fontSize: 13,
      theme: { background: '#0d0d12', foreground: '#00ff9d', cursor: '#00ff9d', selection: 'rgba(0,255,204,0.3)' },
      scrollback: 1000,
    });

    this.fitAddon = new FitAddon.FitAddon();
    this.term.loadAddon(this.fitAddon);
    this.term.open(document.getElementById(this.containerId));
    this.fitAddon.fit();

    this.ws = new WebSocket('ws://' + location.host + '/ws/' + this.scriptName);
    this.ws.onopen = () => this.term.focus();
    this.ws.onmessage = (e) => { this.term.write(e.data.replace(/\n/g, '\r\n')); this.fitAddon.fit(); };
    this.ws.onclose = () => this.term.write('\r\n\r\n[Disconnected]');
    this.ws.onerror = () => this.term.write('\r\n[WebSocket error]');

    this.lineBuf = '';
    this.term.onData((data) => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        const code = data.charCodeAt(0);
        if (code === 127 || code === 8) {
          if (this.lineBuf.length > 0) {
            this.lineBuf = this.lineBuf.slice(0, -1);
            this.term.write('\b \b');
          }
        } else if (code === 13) {
          this.term.write('\n');
          this.ws.send(this.lineBuf + '\n');
          this.lineBuf = '';
        } else if (code >= 32 || code === 9) {
          this.term.write(data);
          this.lineBuf += data;
        }
      }
    });

    document.getElementById(this.containerId).addEventListener('click', () => this.term.focus());
    window.addEventListener('resize', () => this.fitAddon.fit());
  }

  stop() {
    if (this.ws) { this.ws.send('\x03'); this.ws.close(); }
    if (this.term) this.term.write('\r\n[Stopped]\r\n');
    this.started = false;
  }
}

// Create terminal managers for each demo
const terminals = {
  'demo-01': new TerminalManager('terminal-container-01', 'step01_hello_llm.py', 'code-filename-01', 'code-display-01'),
  'demo-02': new TerminalManager('terminal-container-02', 'step02_chat_loop.py', 'code-filename-02', 'code-display-02'),
  'demo-03': new TerminalManager('terminal-container', 'step03_tool_use.py', 'code-filename', 'code-display'),
  'demo-04': new TerminalManager('terminal-container-04', 'step04_agent_loop.py', 'code-filename-04', 'code-display-04'),
  'demo-05': new TerminalManager('terminal-container-05', 'step05_planning.py', 'code-filename-05', 'code-display-05'),
  'demo-06': new TerminalManager('terminal-container-06', 'step06_memory.py', 'code-filename-06', 'code-display-06'),
};

// Observer factory
function createDemoObserver(id) {
  let started = false;
  return new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !started) {
        started = true;
        terminals[id].loadCode();
        terminals[id].start();
      } else if (!entry.isIntersecting && started) {
        terminals[id].stop();
        started = false;
      }
    });
  }, { threshold: 0.1 });
}

// Stop function exposed to HTML buttons
function stopDemo(id) {
  terminals[id].stop();
}

// Restart function — stop then re-load and start
function restartDemo(id) {
  const t = terminals[id];
  t.stop();
  t.loadCode();
  t.start();
}

// Initialize observers
document.addEventListener('DOMContentLoaded', () => {
  const observers = {
    'demo-01': createDemoObserver('demo-01'),
    'demo-02': createDemoObserver('demo-02'),
    'demo-03': createDemoObserver('demo-03'),
    'demo-04': createDemoObserver('demo-04'),
    'demo-05': createDemoObserver('demo-05'),
    'demo-06': createDemoObserver('demo-06'),
  };

  Object.entries(observers).forEach(([id, observer]) => {
    const el = document.getElementById(id);
    if (el) observer.observe(el);
  });
});