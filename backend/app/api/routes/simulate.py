from fastapi import APIRouter, HTTPException
from app.schemas.simulation import SimulationRequest, SimulationResult
from app.simulation.adapter import get_simulator

router = APIRouter()

@router.post("", response_model=SimulationResult)
async def simulate_circuit(req: SimulationRequest):
    try:
        simulator = get_simulator(req.backend)
        schema_dict = req.circuit.model_dump()
        result = simulator.run(schema_dict, req.shots)
        return result
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
