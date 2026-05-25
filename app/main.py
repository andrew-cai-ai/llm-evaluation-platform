from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional
import time
import os

from app.services.openai_service import call_openai
from app.services.anthropic_service import call_anthropic

# Load environment variables
load_dotenv()

print("KEY FOUND:", os.getenv("OPENAI_API_KEY"))

app = FastAPI()


# ----------------------------
# Request Models
# ----------------------------

class EvaluateRequest(BaseModel):
    prompt: str
    provider: str
    model: Optional[str] = None


class ConsistencyRequest(BaseModel):
    prompt: str
    provider: str
    model: Optional[str] = None
    runs: int = 3


# ----------------------------
# Health Check
# ----------------------------

@app.get("/")
def health():
    return {"status": "running"}


# ----------------------------
# Provider Layer
# ----------------------------

def run_provider(
    prompt: str,
    provider: str,
    model: Optional[str]
):
    if provider == "openai":

        result = call_openai(
            prompt=prompt,
            model=model or "gpt-4o-mini"
        )

        return {
            "response": result["text"],
            "token_usage": {
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "total_tokens": result["total_tokens"]
            }
        }

    elif provider == "anthropic":

        response = call_anthropic(
            prompt=prompt,
            model=model or "claude-3-5-haiku-latest"
        )

        return {
            "response": response,
            "token_usage": None
        }

    elif provider == "mock":

        return {
            "response": f"[mock response] {prompt}",
            "token_usage": {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0
            }
        }

    else:
        raise ValueError(
            f"Unsupported provider: {provider}"
        )


# ----------------------------
# Single Evaluation
# ----------------------------

@app.post("/evaluate")
def evaluate(req: EvaluateRequest):

    start = time.time()

    try:

        result = run_provider(
            prompt=req.prompt,
            provider=req.provider,
            model=req.model
        )

        latency_ms = round(
            (time.time() - start) * 1000,
            2
        )

        return {
            "status": "success",
            "provider": req.provider,
            "model": req.model,
            "response": result["response"],
            "latency_ms": latency_ms,
            "token_usage": result["token_usage"]
        }

    except Exception as e:

        latency_ms = round(
            (time.time() - start) * 1000,
            2
        )

        return {
            "status": "failed",
            "provider": req.provider,
            "model": req.model,
            "error_type": type(e).__name__,
            "error": str(e),
            "latency_ms": latency_ms
        }


# ----------------------------
# Consistency Evaluation
# ----------------------------

@app.post("/evaluate/consistency")
def evaluate_consistency(
    req: ConsistencyRequest
):

    start = time.time()

    results = []
    total_tokens = 0

    try:

        for i in range(req.runs):

            run_start = time.time()

            result = run_provider(
                prompt=req.prompt,
                provider=req.provider,
                model=req.model
            )

            run_latency = round(
                (time.time() - run_start) * 1000,
                2
            )

            token_usage = result["token_usage"]

            if (
                token_usage
                and token_usage["total_tokens"]
            ):
                total_tokens += token_usage[
                    "total_tokens"
                ]

            results.append(
                {
                    "run": i + 1,
                    "response": result[
                        "response"
                    ],
                    "latency_ms": run_latency,
                    "token_usage": token_usage
                }
            )

        total_latency = round(
            (time.time() - start) * 1000,
            2
        )

        return {
            "status": "success",
            "provider": req.provider,
            "model": req.model,
            "runs": req.runs,
            "latency_ms": total_latency,
            "total_tokens": total_tokens,
            "results": results
        }

    except Exception as e:

        total_latency = round(
            (time.time() - start) * 1000,
            2
        )

        return {
            "status": "failed",
            "provider": req.provider,
            "model": req.model,
            "runs": req.runs,
            "error_type": type(e).__name__,
            "error": str(e),
            "latency_ms": total_latency
        }