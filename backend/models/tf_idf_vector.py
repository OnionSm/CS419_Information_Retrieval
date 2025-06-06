from pydantic import BaseModel, Field
from typing import Optional, List

class TfIdfVector(BaseModel):
    id: str
    vector_embedding: List[float]

