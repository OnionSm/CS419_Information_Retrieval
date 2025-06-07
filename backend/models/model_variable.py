from pydantic import BaseModel, Field
from typing import Optional, List

class ModelVariable(BaseModel):
    id: str
    docs_quantity: int # doc amount
    terms_quantity: int # term quantity in all doc
    dict_len: int
    k: float
    b: float
    title_multiply: int = 5
    description_multiply: int = 3
    content_multiply: int = 1