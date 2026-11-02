from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.circuit import Circuit
from app.schemas.circuit import CircuitCreate, CircuitResponse

router = APIRouter()

@router.post("", response_model=CircuitResponse)
async def create_circuit(circuit_in: CircuitCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_circuit = Circuit(user_id=current_user.id, title=circuit_in.title, circuit_json=circuit_in.circuit_json)
    db.add(new_circuit)
    await db.commit()
    await db.refresh(new_circuit)
    return new_circuit

@router.get("", response_model=List[CircuitResponse])
async def list_circuits(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).filter(Circuit.user_id == current_user.id))
    return result.scalars().all()

@router.get("/{circuit_id}", response_model=CircuitResponse)
async def get_circuit(circuit_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).filter(Circuit.id == circuit_id, Circuit.user_id == current_user.id))
    circuit = result.scalars().first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit

@router.put("/{circuit_id}", response_model=CircuitResponse)
async def update_circuit(circuit_id: UUID, circuit_in: CircuitCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).filter(Circuit.id == circuit_id, Circuit.user_id == current_user.id))
    circuit = result.scalars().first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    circuit.title = circuit_in.title
    circuit.circuit_json = circuit_in.circuit_json
    await db.commit()
    await db.refresh(circuit)
    return circuit

@router.delete("/{circuit_id}")
async def delete_circuit(circuit_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).filter(Circuit.id == circuit_id, Circuit.user_id == current_user.id))
    circuit = result.scalars().first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    await db.delete(circuit)
    await db.commit()
    return {"message": "Deleted successfully"}
