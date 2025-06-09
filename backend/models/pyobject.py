from pydantic import BaseModel, Field
from typing import List, Any
from bson import ObjectId
from pydantic_core import CoreSchema
from pydantic import GetJsonSchemaHandler

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)

#     @classmethod
#     def __get_pydantic_json_schema__(
#         cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
#     ) -> dict[str, Any]:
#         """
#         Thay thế __modify_schema__ cho Pydantic v2
#         """
#         return {"type": "string", "format": "objectid"}


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):  # Thêm tham số info cho Pydantic v2
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """
        Thay thế __modify_schema__ cho Pydantic v2
        """
        return {"type": "string", "format": "objectid"}
