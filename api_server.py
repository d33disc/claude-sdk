"""
API server for the Claude SDK.
"""

import os
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union

from claude_sdk import Claude

app = FastAPI(title="Claude SDK API Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the API key from the environment
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

# Create a Claude client
claude = Claude(api_key=API_KEY)

class GenerateRequest(BaseModel):
    """
    Request model for the generate endpoint.
    """
    model: str
    prompt: str
    max_tokens: int = 1000
    temperature: float = 0.7
    system_prompt: Optional[str] = None
    stream: bool = False
    tools: Optional[List[Dict[str, Any]]] = None

class MessageRequest(BaseModel):
    """
    Request model for the messages endpoint.
    """
    model: str
    messages: List[Dict[str, Union[str, List[Dict[str, str]]]]]
    max_tokens: int = 1000
    temperature: float = 0.7
    system: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None
    stream: bool = False

class ComputeUseRequest(BaseModel):
    """
    Request model for the compute_use endpoint.
    """
    model: str
    prompt: str
    max_tokens: int = 1000
    temperature: float = 0.7
    system_prompt: Optional[str] = None

@app.post("/generate")
async def generate(request: GenerateRequest):
    """
    Generate a response from Claude.
    """
    try:
        response = claude.generate(
            model=request.model,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system_prompt=request.system_prompt,
            stream=request.stream,
            tools=request.tools,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/messages")
async def messages(request: MessageRequest):
    """
    Create a message using the Claude API.
    """
    try:
        response = claude.messages_create(
            model=request.model,
            messages=request.messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system=request.system,
            tools=request.tools,
            stream=request.stream,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compute_use")
async def compute_use(request: ComputeUseRequest):
    """
    Use Claude's computer use feature to perform desktop automation.
    """
    try:
        response = claude.compute_use(
            model=request.model,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system_prompt=request.system_prompt,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "Claude SDK API Server",
        "docs": "/docs",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
