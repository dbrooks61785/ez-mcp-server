from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json

app = FastAPI()

# ---- REQUIRED FOR CHATGPT MCP ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PingResponse(BaseModel):
    message: str

@app.post("/ping", response_model=PingResponse)
def ping():
    return {"message": "pong"}

@app.get("/sse")
async def sse(request: Request):
    async def event_stream():
        # Required: send first SSE event immediately
        yield "event: message\ndata: {\"status\":\"ready\"}\n\n"

        # Keep connection alive
        while True:
            yield "event: message\ndata: {\"status\":\"alive\"}\n\n"
            await asyncio.sleep(1)

    # Required headers for SSE & MCP
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        },
    )
