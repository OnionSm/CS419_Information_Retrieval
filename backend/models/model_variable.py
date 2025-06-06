from pydantic import BaseModel, Field
from typing import Optional, List

class ModelVariable(BaseModel):
    id: str
    avgl: float
    k: float
    b: float
    