import asyncio
import json
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ============================
# CONFIG
# ============================
BEARER_TOKEN = "EZ_AUTOMATION_MCP_SERVER_DONT_STEAL_MY_SHIT_2025"

def verify_token(auth_header: str | None):
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = auth_header.replace("Bearer ", "").strip()

    if token != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")


# ============================
# APP INIT
# ============================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================
# MCP ENDPOINTS
# ============================

@app.get("/mcp/info")
async def mcp_info(authorization: str | None = Header(default=None)):
    verify_token(authorization)
    return {
        "protocol": "2024-02-01",
        "name": "EZ Automation MCP",
        "version": "1.0.0",
        "tools": ["ping"]
    }


@app.get("/mcp/tools")
async def m
