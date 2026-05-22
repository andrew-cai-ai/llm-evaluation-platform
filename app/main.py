from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import time
from typing import Optional

from app.services.openai_service import call_openai
from app.services.anthropic_service import call_anthropic

load_dotenv()

app = FastAPI()


class EvaluateRequest(BaseModel):
    prompt: str
    provider: str
    model: Optional[str] = None


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/evaluate")
def evaluate(req: EvaluateRequest):
    start = time.time()

    if req.provider == "openai":
        response = call_openai(
            prompt=req.prompt,
            model=req.model or "gpt-4o-mini"
        )
    elif req.provider == "anthropic":
        response = call_anthropic(
            prompt=req.prompt,
            model=req.model or "claude-3-5-haiku-latest"
        )
    else:
        return {"error": "Unsupported provider"}

    latency_ms = round((time.time() - start) * 1000, 2)

    return {
        "provider": req.provider,
        "model": req.model,
        "response": response,
        "latency_ms": latency_ms
    }