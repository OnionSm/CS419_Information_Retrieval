from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from typing import List
from models.news import News
from pymongo.database import Database
from services import news_service
from models.news import News, NewsRespone
from services import text_preprocess

async def search(query: str, model: str) -> NewsRespone:
    try:
        tokens = text_preprocess.process_text(query)
        if model == "tf-idf":
            pass
        elif model == "bm25":
            pass
        pass
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi không mong muốn khi truy vấn: {e}")