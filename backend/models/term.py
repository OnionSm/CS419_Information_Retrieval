from pydantic import BaseModel, Field
from typing import Optional, List

class Term(BaseModel):
    id: str
    term_name: str
    count_rl_docs: int = 1
    related_docs: List[str] = Field(default_factory=list)

class TermInput(BaseModel):
    pass
    
class TermFrequency(BaseModel):
    term_name: str
    frequency: int

class TermIDF(BaseModel):
    id_term: str
    idf: float