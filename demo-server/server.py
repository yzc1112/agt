"""
Demo Server — runs real Python scripts via WebSocket + xterm.js
FastAPI + uvicorn for local presentation demos.

Run: cd demo-server && pip install fastapi uvicorn websockets && uvicorn server:app --reload
Then open: http://localhost:8000
"""
import asyncio
import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGT_DIR = os.path.join(BASE_DIR, "..", "scripts")
STATIC_DIR = os.path.join(BASE_DIR, "static")


@app.websocket("/ws/{script_name}")
async def run_script(ws: WebSocket, script_name: str):
    """Run a Python script, piping stdin/stdout over WebSocket."""
    await ws.accept()

    # Security: only allow safe filenames
    safe_name = os.path.basename(script_name)
    if not all(c.isalnum() or c in "-_." for c in safe_name):
        await ws.send_text("Error: invalid script name\n")
        await ws.close()
        return

    script_path = os.path.join(AGT_DIR, safe_name)
    if not os.path.exists(script_path):
        await ws.send_text(f"Error: script not found: {safe_name}\n")
        await ws.close()
        return

    await ws.send_text(f"$ {sys.executable} {safe_name}\n\n")

    # Use piped subprocess — xterm.js handles all line editing locally
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-u", script_path,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=AGT_DIR,
        env=None,  # Inherit full environment so venv site-packages are found
    )

    async def pipe_output():
        try:
            while True:
                chunk = await proc.stdout.read(256)
                if not chunk:
                    break
                try:
                    await ws.send_text(chunk.decode(errors="replace"))
                except Exception:
                    break
        except Exception:
            pass
        finally:
            try:
                proc.kill()
            except Exception:
                pass

    out_task = asyncio.create_task(pipe_output())

    try:
        while True:
            msg = await ws.receive_text()
            if msg:
                proc.stdin.write(msg.encode())
                await proc.stdin.drain()
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        out_task.cancel()
        try:
            proc.kill()
        except Exception:
            pass
        try:
            await proc.wait()
        except Exception:
            pass


@app.get("/")
async def get_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/step/{name}")
async def get_step(name: str):
    path = os.path.join(AGT_DIR, name)
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "not found"}


# Serve static files at root (not /static) so relative paths work for both file:// and http://
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
