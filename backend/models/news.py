from pydantic import BaseModel, Field
from typing import Optional, List

class News(BaseModel):
    id: str
    title: str
    description: str
    content: str
    token: List[str]
    link: str

class NewsRespone(BaseModel):
    title: str
    description: str
    content: str
    link: str
    score: str