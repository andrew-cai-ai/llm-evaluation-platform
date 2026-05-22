from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI()

class EvaluateRequest(BaseModel):
    prompt: str
    model: str


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/evaluate")
def evaluate(req: EvaluateRequest):

    start=time.time()

    # temporary mock response
    response=f"Received prompt: {req.prompt}"

    latency=(time.time()-start)*1000

    return {
        "model":req.model,
        "response":response,
        "latency_ms":round(latency,2)
    }