from typing import List, Optional
from models.term import Term
from models.tf_idf_vector import TfIdfVector
from ..database import client, db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError, DuplicateKeyError
from bson import ObjectId 

async def create_single_doc_embedding(tf_idf_vector_data: TfIdfVector) -> TfIdfVector:
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    tfidf_collection = db.tfidf
    try:
        tf_idf_vector_data = tf_idf_vector_data.model_dump(by_alias=True, exclude_unset=True)
        if "_id" in tf_idf_vector_data:
            del tf_idf_vector_data["_id"]
        result = tfidf_collection.insert_one(tf_idf_vector_data)
        inserted_vector_data = tfidf_collection.find_one({"_id": result.inserted_id})
        if not inserted_vector_data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                 detail="Failed to retrieve inserted new vector data.")
        inserted_vector_data['id'] = str(inserted_vector_data["_id"])
        del inserted_vector_data["_id"]
        print(f"Đã thêm tin tức thành công với _id: {result.inserted_id}")
        return inserted_vector_data
    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"Term item with unique key already exists: {e.details.get('errmsg', 'Unknown duplicate key error')}")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Database error during term creation: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"An unexpected error occurred: {e}")

async def create_multi_doc_embedding(list_doc_embedding: List[TfIdfVector]):
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    tfidf_collection = db.tfidf
    vector_to_insert = []
    for doc in list_doc_embedding:
        new_doc_embedding = doc.model_dump(by_alias= True, exclude_unset= True)
        if "_id" in new_doc_embedding:
            del new_doc_embedding["_id"]
        vector_to_insert.append(new_doc_embedding)
    try:
        if not vector_to_insert:
            return {"message": "Do not have any tfidf vector to insert"}
        result = tfidf_collection.insert_many(vector_to_insert)
        inserted_ids = [str(obj_id) for obj_id in result.inserted_ids]
        return {
            "message": f"Insert {len(inserted_ids)} embedding completely.",
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

async def get_single_embedd_doc_by_id_async(doc_id: str) -> TfIdfVector:
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    tfidf_collection = db.tfidf
    try: 
        obj_id = ObjectId(doc_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="ID tin tức không hợp lệ. Vui lòng cung cấp một ObjectId hợp lệ.")
    
    try:
        embedd_doc = tfidf_collection.find({"_id": obj_id})
        if embedd_doc:
            embedd_doc["id"] = str(embedd_doc["_id"])
            return TfIdfVector(**embedd_doc)
        return None 
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database khi lấy tin tức theo ID: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi không mong muốn khi lấy tin tức theo ID: {e}")

async def get_multi_embedd_doc_by_id_async(list_docs_id: List[str]) -> List[TfIdfVector]:
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    tfidf_collection = db.tfidf

    embedd_doc_res = []
    list_obj_id = []
    try: 
        for doc_id in list_docs_id:
            obj_id = ObjectId(doc_id)
            list_obj_id.append(obj_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"ID {obj_id} không hợp lệ. Vui lòng cung cấp một ObjectId hợp lệ.")
    
    try:
        for obj_id in list_obj_id:
            embedd_doc = tfidf_collection.find_one({"_id": obj_id})
            if embedd_doc:
                embedd_doc["id"] = str(embedd_doc["_id"])
                embedd_doc_res.append(TfIdfVector(**embedd_doc))
        return embedd_doc_res
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database khi lấy tin tức theo ID: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi không mong muốn khi lấy tin tức theo ID: {e}")



