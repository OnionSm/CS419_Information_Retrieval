from pydantic import BaseModel, Field
from typing import Optional, List

class Term(BaseModel):
    id: str
    term_name: str
    idf: int
    related_docs: List[str] = []

