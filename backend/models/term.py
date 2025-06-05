from pydantic import BaseModel, Field
from typing import Optional, List

class Term(BaseModel):
    id: str
    term: str
    related_docs: List[int] = []

