from pydantic import BaseModel, Field
from typing import Optional, List
from models.term import TermFrequency

class News(BaseModel):
    id: str
    title: str
    description: str
    content: str
    terms: List[TermFrequency] = Field(default_factory=list)
    doc_size: int
    link: str
    

class NewsRespone(BaseModel):
    title: str
    description: str
    content: str
    link: str
    score: str

class NewsInput(BaseModel):
    title: str
    description: str
    content: str
    link: str