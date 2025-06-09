from pydantic import BaseModel, Field
from typing import Optional, List
from models.pyobject import PyObjectId
from bson import ObjectId

# class Term(BaseModel):
#     id: str
#     term_name: str
#     count_rl_docs: int = 1
#     related_docs: List[str] = Field(default_factory=list)

class Term(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    idx: int
    term_name: str
    count_rl_docs: int = 1
    related_docs: List[PyObjectId] = Field(default_factory=list)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TermInput(BaseModel):
    pass
    
class TermFrequency(BaseModel):
    term_name: str
    frequency: float

class TermIDF(BaseModel):
    id_term: str
    idf: float