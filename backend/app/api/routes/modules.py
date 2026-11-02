from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.module import Module
from app.schemas.module import ModuleResponse, ModuleListItem

router = APIRouter()

@router.get("", response_model=List[ModuleListItem])
async def list_modules(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).order_by(Module.order_index))
    return result.scalars().all()

@router.get("/{slug}", response_model=ModuleResponse)
async def get_module(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).filter(Module.slug == slug))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module
