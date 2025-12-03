from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json

app = FastAPI()

class PingResponse(BaseModel):
    message: str

@app.post("/ping", response_model=PingResponse)
def ping():
    return {"message": "pong"}

@app.get("/sse")
async def sse(request: Request):
    async def event_stream():
        # SEND FIRST EVENT IMMEDIATELY (required by ChatGPT)
        yield f"data: {json.dumps({'status': 'ready'})}\n\n"

        # KEEP ALIVE EVENTS
        while True:
            yield f"data: {json.dumps({'status': 'alive'})}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
