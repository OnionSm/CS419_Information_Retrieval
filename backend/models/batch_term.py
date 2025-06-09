from pydantic import BaseModel, Field
from typing import Optional, List
from models.term import TermFrequency
from models.pyobject import PyObjectId
from bson import ObjectId

class BatchTerm(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    idx: int
    term_name: str
    count_docs: int
    idf: float = 0
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}