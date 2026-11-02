from fastapi import APIRouter, Request, HTTPException
from app.schemas.ai import AIRequest, AIResponse
from app.ai.tutor import GeminiTutor
from pydantic import BaseModel
import time

router = APIRouter()
tutor = GeminiTutor()

rate_limits = {}

def check_rate_limit(ip: str):
    now = time.time()
    if ip not in rate_limits:
        rate_limits[ip] = []
    # Filter out requests older than 60 seconds
    rate_limits[ip] = [t for t in rate_limits[ip] if now - t < 60]
    if len(rate_limits[ip]) >= 20:
        raise HTTPException(status_code=429, detail="Too many requests")
    rate_limits[ip].append(now)

class DebugRequest(BaseModel):
    circuit_json: str
    error_msg: str

class GenerateRequest(BaseModel):
    description: str

@router.post("/explain", response_model=AIResponse)
async def explain(req: AIRequest, request: Request):
    check_rate_limit(request.client.host)
    answer = await tutor.explain(req.question, req.context or "", req.mode)
    return AIResponse(answer=answer, mode=req.mode)

@router.post("/debug", response_model=AIResponse)
async def debug(req: DebugRequest, request: Request):
    check_rate_limit(request.client.host)
    answer = await tutor.debug_circuit(req.circuit_json, req.error_msg)
    return AIResponse(answer=answer, mode="debug")

@router.post("/generate-code")
async def generate_code(req: GenerateRequest, request: Request):
    check_rate_limit(request.client.host)
    code = await tutor.generate_code(req.description)
    return {"code": code}
