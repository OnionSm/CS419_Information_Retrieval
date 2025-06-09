from pydantic import BaseModel, Field
from typing import Optional, List
from models.pyobject import PyObjectId
from bson import ObjectId

class ModelVariable(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    docs_quantity: int # doc amount
    terms_quantity: int # term quantity in all doc
    dict_len: int
    k: float
    b: float
    title_multiply: int = 5
    description_multiply: int = 3
    content_multiply: int = 1

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
