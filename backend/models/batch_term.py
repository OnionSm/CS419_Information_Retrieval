from pydantic import BaseModel, Field
from typing import Optional, List

class BatchTerm(BaseModel):
    id: str
    term_name: str
    count_docs: int
    idf: float = 0
    