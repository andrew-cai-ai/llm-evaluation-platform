from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import time
from typing import Optional
import traceback
from app.services.openai_service import call_openai
from app.services.anthropic_service import call_anthropic
import os

print("KEY FOUND:", os.getenv("OPENAI_API_KEY"))
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
    token_usage = None

    try:
        if req.provider == "openai":
            result = call_openai(
                prompt=req.prompt,
                model=req.model or "gpt-4o-mini"
            )
            response = result["text"]
            token_usage = {
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "total_tokens": result["total_tokens"],
            }

        elif req.provider == "anthropic":
            response = call_anthropic(
                prompt=req.prompt,
                model=req.model or "claude-3-5-haiku-latest"
            )

        elif req.provider == "mock":
            response = f"[mock response] {req.prompt}"

        else:
            return {
                "status": "failed",
                "error": "Unsupported provider",
                "provider": req.provider
            }

        latency_ms = round((time.time() - start) * 1000, 2)

        return {
            "status": "success",
            "provider": req.provider,
            "model": req.model,
            "response": response,
            "latency_ms": latency_ms,
            "token_usage": token_usage,
        }

    except Exception as e:
        latency_ms = round((time.time() - start) * 1000, 2)

        return {
            "status": "failed",
            "provider": req.provider,
            "model": req.model,
            "error": str(e),
            "details": traceback.format_exc(),
            "latency_ms": latency_ms,
            "token_usage": token_usage,
        }