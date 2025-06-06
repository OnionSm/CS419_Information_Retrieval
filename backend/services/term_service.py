from typing import List, Optional
from models.term import Term
from ..database import client, db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError, DuplicateKeyError
from bson import ObjectId 

async def create_single_term_async(term: Term) -> Term:
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    term_collection = db.term
    try:
        new_term = term.model_dump(by_alias=True, exclude_unset=True)
        if "_id" in new_term:
            del new_term["_id"]
        result = term_collection.insert_one(new_term)
        inserted_term = term_collection.find_one({"_id": result.inserted_id})
        if not inserted_term:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                 detail="Failed to retrieve inserted new term.")
        inserted_term['id'] = str(inserted_term["_id"])
        del inserted_term["_id"]
        print(f"Đã thêm tin tức thành công với _id: {result.inserted_id}")
        return inserted_term
    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"Term item with unique key already exists: {e.details.get('errmsg', 'Unknown duplicate key error')}")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Database error during term creation: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"An unexpected error occurred: {e}")
    

async def create_multi_term_async(list_term: List[Term]):
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    term_collection = db.term
    terms_to_insert = []
    for term_item in list_term:
        new_term = term_item.model_dump(by_alias= True, exclude_unset= True)
        if "_id" in new_term:
            del new_term["_id"]
        terms_to_insert.append(new_term)

    try: 
        if not terms_to_insert:
            return {"message": "Do not have any term to insert"}
        result = term_collection.insert_many(terms_to_insert)
        inserted_ids = [str(obj_id) for obj_id in result.inserted_ids]
        return {
            "message": f"Insert {len(inserted_ids)} term completely.",
            "inserted_ids": inserted_ids
        }
    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Một số tin tức có giá trị trùng lặp (ví dụ: tiêu đề duy nhất): {e.details.get('errmsg', 'Unknown duplicate key error')}")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database trong quá trình tạo tin tức hàng loạt: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Một lỗi không mong muốn đã xảy ra: {e}")


async def get_terms_data_by_id_async(term_id: str):
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    term_collection = db.term
    try:
        obj_id = ObjectId(term_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="ID tin tức không hợp lệ. Vui lòng cung cấp một ObjectId hợp lệ.")
    
    try:
        term_data = term_collection.find_one({"_id": obj_id})
        if term_data:
            term_data["id"] = str(term_data["_id"])
            return Term(**term_data)
        return None
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database khi lấy tin tức theo ID: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi không mong muốn khi lấy tin tức theo ID: {e}")


async def get_term_data_by_name_async(term_name: str):
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    term_collection = db.term
    
    try:
        term_data = term_collection.find_one({"term_name": term_name})
        if term_data:
            term_data["id"] = str(term_data["_id"])
            return Term(**term_data)
        return None
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database khi lấy tin tức theo ID: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi không mong muốn khi lấy tin tức theo ID: {e}")


async def update_full_term_async(term_id : str, term_data: Term):
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    term_collection = db.term

    try:
        obj_id = ObjectId(term_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="ID tin tức không hợp lệ. Vui lòng cung cấp một ObjectId hợp lệ.")
    
    update_data = term_data.model_dump(by_alias=True, exclude_unset=True)
    if '_id' in update_data:
        del update_data['_id']
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Không có dữ liệu để cập nhật.")
    try:
        result = term_collection.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            return None 
        updated_term_data = term_collection.find_one({"_id": obj_id})
        if updated_term_data:
            updated_term_data['id'] = str(updated_term_data['_id'])
            return Term(**updated_term_data)
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Không thể lấy tin tức sau khi cập nhật.")

    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Cập nhật thất bại: Giá trị duy nhất bị trùng lặp: {e.details.get('errmsg', 'Unknown duplicate key error')}")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database khi cập nhật tin tức: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi không mong muốn khi cập nhật tin tức: {e}")
    

async def add_docs_to_related_docs(term_id: str, list_docs: List[str]):
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    term_collection = db.term

    try:
        obj_id = ObjectId(term_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="ID tin tức không hợp lệ. Vui lòng cung cấp một ObjectId hợp lệ.")
    try:
        term_data = term_collection.find_one({"_id": obj_id})
        current_related_docs = term_data["related_docs"]
        current_related_docs.extend(list_docs)
        term_data["related_docs"] = current_related_docs
        if "_id" in term_data:
            del term_data["_id"]
        result = term_collection.update_one(
            {"_id": obj_id},
            {"$set": term_data}
        )
        if result.matched_count == 0:
            return None 
        updated_term_data = term_collection.find_one({"_id": obj_id})
        if updated_term_data:
            updated_term_data['id'] = str(updated_term_data['_id'])
            return Term(**updated_term_data)
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Không thể lấy tin tức sau khi cập nhật.")

    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Cập nhật thất bại: Giá trị duy nhất bị trùng lặp: {e.details.get('errmsg', 'Unknown duplicate key error')}")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database khi cập nhật tin tức: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi không mong muốn khi cập nhật tin tức: {e}")