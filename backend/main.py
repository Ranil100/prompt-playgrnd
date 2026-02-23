import os
import time
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai

from prompts import build_prompt
from evaluator import evaluate_outputs

load_dotenv()

app = FastAPI(title="Prompt Playground API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class ExperimentRequest(BaseModel):
    task: str = Field(..., min_length=3)
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)


class PromptResult(BaseModel):
    strategy: str
    prompt: str
    output: str
    latency_ms: int
    score: int


class ExperimentResponse(BaseModel):
    task: str
    results: list[PromptResult]
    winner: str
    winner_reason: str


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is missing. Add it to your .env file."
        )
    return genai.Client(api_key=api_key)


def generate(client, prompt: str, temperature: float) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"temperature": temperature},
    )
    return (response.text or "").strip()


@app.get("/api/health")
def health():
    return {"status": "ok", "model": MODEL}


@app.post("/api/experiment", response_model=ExperimentResponse)
def run_experiment(request: ExperimentRequest):
    client = get_client()
    strategies = ["zero-shot", "few-shot", "structured"]
    results = []

    for strategy in strategies:
        prompt = build_prompt(strategy, request.task)
        started = time.perf_counter()
        try:
            output = generate(client, prompt, request.temperature)
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Gemini API error: {exc}")
        latency = round((time.perf_counter() - started) * 1000)
        results.append({
            "strategy": strategy,
            "prompt": prompt,
            "output": output,
            "latency_ms": latency,
            "score": 0,
        })

    evaluated, winner, reason = evaluate_outputs(request.task, results)
    return {
        "task": request.task,
        "results": evaluated,
        "winner": winner,
        "winner_reason": reason,
    }
