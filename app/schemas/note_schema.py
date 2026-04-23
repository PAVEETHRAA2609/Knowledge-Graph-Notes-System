from pydantic import BaseModel
from typing import List, Optional


class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = ""
    tags: List[str] = []


class NoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    tags: List[str]

    class Config:
        from_attributes = True