from pydantic import BaseModel, field_validator
from typing import Optional, Any, Dict, Union
from uuid import UUID
import json


class ModuleResponse(BaseModel):
    id: UUID
    slug: str
    title: str
    description: Optional[str]
    order_index: int
    content_json: Dict[str, Any]

    class Config:
        from_attributes = True

    @field_validator("content_json", mode="before")
    @classmethod
    def parse_content(cls, v: Any) -> Dict[str, Any]:
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {}
        return {}


class ModuleListItem(BaseModel):
    id: UUID
    slug: str
    title: str
    description: Optional[str]
    order_index: int

    class Config:
        from_attributes = True
