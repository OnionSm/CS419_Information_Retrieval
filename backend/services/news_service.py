from typing import List, Optional
from models.news import News
from ..database import client, db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError, DuplicateKeyError
from bson import ObjectId 

async def create_single_news_async(news: News):
    """
    Thêm một tin tức mới vào collection 'news' trong MongoDB.

    Args:
        news (News): Đối tượng News cần thêm vào database.

    Returns:
        dict: Tài liệu tin tức đã được thêm vào, bao gồm _id được tạo bởi MongoDB.

    Raises:
        HTTPException: Nếu có lỗi xảy ra trong quá trình chèn dữ liệu vào database
                       (ví dụ: lỗi kết nối, lỗi trùng lặp, lỗi chung).
    """
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Database connection not established.")
    news_collection = db.News
    try:
        news_data = news.model_dump(by_alias=True, exclude_unset=True) 
        if '_id' in news_data:
            del news_data['_id']

        result = news_collection.insert_one(news_data)
        inserted_news = news_collection.find_one({"_id": result.inserted_id})
        if not inserted_news:
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                 detail="Failed to retrieve inserted news item.")
        inserted_news['id'] = str(inserted_news['_id'])
        del inserted_news['_id'] 
        print(f"Đã thêm tin tức thành công với _id: {result.inserted_id}")
        return inserted_news
    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"News item with unique key already exists: {e.details.get('errmsg', 'Unknown duplicate key error')}")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Database error during news creation: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"An unexpected error occurred: {e}")


async def create_multi_news_async(list_news: List[News]):
    """
    Thêm nhiều tin tức mới vào collection 'news' trong MongoDB.

    Args:
        list_news (List[News]): Một danh sách các đối tượng News cần thêm vào database.

    Returns:
        dict: Một dictionary chứa thông báo thành công và danh sách các _id đã được chèn.

    Raises:
        HTTPException: Nếu có lỗi xảy ra trong quá trình chèn dữ liệu vào database
                       (ví dụ: lỗi kết nối, lỗi trùng lặp, lỗi chung).
    """
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database connection not established.")

    news_collection = db.news 

    documents_to_insert = []
    for news_item in list_news:
        news_data = news_item.model_dump(by_alias=True, exclude_unset=True)
        if '_id' in news_data:
            del news_data['_id']
        documents_to_insert.append(news_data)

    try:
        if not documents_to_insert:
            return {"message": "Không có tin tức nào để thêm."}
        result = news_collection.insert_many(documents_to_insert)
        inserted_ids = [str(obj_id) for obj_id in result.inserted_ids]

        print(f"Đã thêm thành công {len(inserted_ids)} tin tức.")
        return {
            "message": f"Đã thêm thành công {len(inserted_ids)} tin tức.",
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


async def get_news_by_id_async(news_id: str) -> Optional[News]:
    """
    Lấy một tin tức theo ID từ collection 'news'.

    Args:
        news_id (str): ID của tin tức (chuỗi ObjectId).

    Returns:
        Optional[News]: Đối tượng News nếu tìm thấy, ngược lại là None.

    Raises:
        HTTPException: Nếu database connection không được thiết lập, 
                       ID không hợp lệ, hoặc có lỗi database.
    """
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database connection not established.")

    news_collection = db.news
    try:
        obj_id = ObjectId(news_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="ID tin tức không hợp lệ. Vui lòng cung cấp một ObjectId hợp lệ.")
    try:
        news_data = news_collection.find_one({"_id": obj_id})
        if news_data:
            news_data['id'] = str(news_data['_id'])
            return News(**news_data) 
        return None
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database khi lấy tin tức theo ID: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi không mong muốn khi lấy tin tức theo ID: {e}")

async def get_news_by_link_async(link: str) -> Optional[News]:
    """
    Lấy một tin tức theo URL/link từ collection 'news'.
    Giả định rằng trường 'link' là duy nhất (hoặc bạn muốn lấy bản đầu tiên).

    Args:
        link (str): Link của tin tức.

    Returns:
        Optional[News]: Đối tượng News nếu tìm thấy, ngược lại là None.

    Raises:
        HTTPException: Nếu database connection không được thiết lập hoặc có lỗi database.
    """
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database connection not established.")

    news_collection = db.news

    try:
        news_data = news_collection.find_one({"link": link})
        if news_data:
            news_data['id'] = str(news_data['_id'])
            return News(**news_data)
        return None
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database khi lấy tin tức theo link: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi không mong muốn khi lấy tin tức theo link: {e}")

async def update_news_by_id_async(news_id: str, news_update: News) -> Optional[News]:
    """
    Cập nhật thông tin của một tin tức theo ID.

    Args:
        news_id (str): ID của tin tức cần cập nhật (chuỗi ObjectId).
        news_update (News): Đối tượng News chứa các trường muốn cập nhật.

    Returns:
        Optional[News]: Đối tượng News sau khi được cập nhật, hoặc None nếu không tìm thấy.

    Raises:
        HTTPException: Nếu database connection không được thiết lập, ID không hợp lệ,
                       hoặc có lỗi database.
    """
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database connection not established.")

    news_collection = db.News

    try:
        obj_id = ObjectId(news_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="ID tin tức không hợp lệ. Vui lòng cung cấp một ObjectId hợp lệ.")

    update_data = news_update.model_dump(by_alias=True, exclude_unset=True)
    
    if '_id' in update_data:
        del update_data['_id']

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Không có dữ liệu để cập nhật.")

    try:
        result = news_collection.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            return None 
        updated_news_data = news_collection.find_one({"_id": obj_id})
        if updated_news_data:
            updated_news_data['id'] = str(updated_news_data['_id'])
            return News(**updated_news_data)
        
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

async def delete_news_by_id_async(news_id: str) -> bool:
    """
    Xóa một tin tức theo ID khỏi collection 'news'.

    Args:
        news_id (str): ID của tin tức cần xóa (chuỗi ObjectId).

    Returns:
        bool: True nếu tin tức được xóa thành công, False nếu không tìm thấy.

    Raises:
        HTTPException: Nếu database connection không được thiết lập, ID không hợp lệ,
                       hoặc có lỗi database.
    """
    if db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database connection not established.")

    news_collection = db.news

    try:
        obj_id = ObjectId(news_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="ID tin tức không hợp lệ. Vui lòng cung cấp một ObjectId hợp lệ.")

    try:
        result = news_collection.delete_one({"_id": obj_id})
        
        if result.deleted_count == 1:
            print(f"Đã xóa tin tức thành công với _id: {news_id}")
            return True
        return False 
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi database khi xóa tin tức: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Lỗi không mong muốn khi xóa tin tức: {e}")