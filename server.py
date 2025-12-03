import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ---- MCP REQUIRED ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/mcp/info")
async def mcp_info():
    return {
        "protocol": "2024-02-01",
        "name": "EZ Automation MCP",
        "version": "1.0.0",
        "tools": ["ping"]
    }

@app.get("/mcp/tools")
async def mcp_tools():
    return {
        "tools": {
            "ping": {
                "name": "ping",
                "description": "Responds with pong",
                "schema": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    }

@app.post("/mcp/execute")
async def mcp_execute(request: Request):
    body = await request.json()
    tool = body.get("tool")
    if tool == "ping":
        return JSONResponse({"response": {"message": "pong"}})
    return JSONResponse({"error": "Unknown tool"}, status_code=400)

@app.get("/sse")
async def sse():
    async def stream():
        yield "event: ready\ndata: {}\n\n"
        while True:
            yield "event: keepalive\ndata: {}\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(stream(), media_type="text/event-stream")
