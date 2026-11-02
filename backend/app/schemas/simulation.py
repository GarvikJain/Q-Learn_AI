from pydantic import BaseModel
from typing import Dict, List, Optional
from app.schemas.circuit import CircuitSchema

class SimulationRequest(BaseModel):
    circuit: CircuitSchema
    backend: str = 'qiskit_aer'
    shots: int = 1024

class SimulationResult(BaseModel):
    counts: Dict[str, int]
    statevector: Optional[List[List[float]]] = None
    probabilities: Dict[str, float]
    execution_time_ms: float
    backend_used: str
    num_qubits: int
