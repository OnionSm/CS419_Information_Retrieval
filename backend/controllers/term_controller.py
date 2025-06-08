from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from typing import List
from models.news import News, NewsInput, NewsRespone
from pymongo.database import Database
from services import news_service
