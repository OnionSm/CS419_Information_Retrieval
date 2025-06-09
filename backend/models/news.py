from pydantic import BaseModel, Field
from typing import Optional, List
from models.term import TermFrequency
from models.pyobject import PyObjectId
from bson import ObjectId

# class News(BaseModel):
#     id: str
#     title: str
#     description: str
#     content: str
#     terms: List[TermFrequency] = Field(default_factory=list)
#     doc_size: int
#     link: str
    
class News(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    content: str
    terms: List[TermFrequency] = Field(default_factory=list)
    doc_size: int
    link: str
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class NewsRespone(BaseModel):
    title: str
    description: str
    content: str
    link: str
    score: float

class NewsInput(BaseModel):
    title: str
    description: str
    content: str
    link: str