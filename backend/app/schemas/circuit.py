from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class GateSchema(BaseModel):
    type: str
    targets: List[int]
    control: Optional[int] = None
    controls: Optional[List[int]] = None
    step: int

class CircuitSchema(BaseModel):
    num_qubits: int
    gates: List[GateSchema]
    metadata: Optional[Dict[str, Any]] = None

class CircuitCreate(BaseModel):
    title: str
    circuit_json: str

class CircuitResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    circuit_json: str
    created_at: datetime

    class Config:
        from_attributes = True
