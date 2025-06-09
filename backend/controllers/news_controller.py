from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from typing import List
from models.news import News, NewsInput, NewsRespone
from pymongo.database import Database
from services import news_service

router = APIRouter(
    prefix="/news",
    tags=["news"],
    responses={404: {"description": "Not found"}},
)

@router.post("/single", response_model=NewsRespone, status_code=status.HTTP_201_CREATED)
async def create_single_news(news: NewsInput) -> NewsRespone:
    try:
        created_news_data_dict = await news_service.create_single_news_async(news)
        return NewsRespone(**created_news_data_dict)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi không mong muốn khi truy vấn: {e}")

@router.post("/multi", status_code=status.HTTP_201_CREATED)
async def create_multi_news(list_news: List[News]) -> str:
    try:
        message = await news_service.create_multi_news_async(list_news)
        return message
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi không mong muốn khi truy vấn: {e}")
    
@router.get("/{news_id}", response_model=News, status_code=status.HTTP_200_OK)
async def get_news_by_id(news_id: str) -> News:
    try:
        news = await news_service.get_news_by_id_async(news_id)
        return news
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi không mong muốn khi truy vấn: {e}")


# @router.put("/{news_id}",response_model=News, status_code=status.HTTP_200_OK)
# async def update_new_by_id(news_id: str,news_update: News) -> News:
#     try:
#         news = await news_service.update_news_by_id_async(news_id, news_update)
#         return news
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi không mong muốn khi truy vấn: {e}")

# @router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_news_by_id(news_id: str):
#     try:
#         res = await news_service.delete_news_by_id_async(news_id)
#         if not res:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Tin tức với ID '{news_id}' không tìm thấy để xóa."
#             )
#         return
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi không mong muốn khi xóa tin tức: {e}")