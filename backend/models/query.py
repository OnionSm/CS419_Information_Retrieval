from pydantic import BaseModel, Field
from typing import Optional, List
from models.pyobject import PyObjectId
from bson import ObjectId

class QueryInput(BaseModel):
    query: str
    model: str = "tf-idf"
    top_n: int = 5