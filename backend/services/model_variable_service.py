from typing import List, Dict, Any, Optional
from models.term import Term
from ..database import client, db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError, DuplicateKeyError
from bson import ObjectId 
from models.batch_term import BatchTerm
from models.model_variable import ModelVariable

async def get_model_variable() -> ModelVariable:
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    variable_collection = db.model_variable
    try:
        setting = variable_collection.find_one({})
        if not setting:
            raise HTTPException(status_code=404, detail="Không tìm thấy cấu hình")
        if "_id" in setting:
            del setting["_id"]
        return setting

    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Một số cài đặt trùng lặp: {getattr(e, 'details', {}).get('errmsg', 'Unknown duplicate key error')}")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Một lỗi không mong muốn đã xảy ra: {e}")