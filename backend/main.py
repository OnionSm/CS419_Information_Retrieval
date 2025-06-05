from fastapi import FastAPI, HTTPException, Depends
from typing import List
import os
import database
from controllers import news_controller
app = FastAPI()


database.connect_to_mongodb()

if database.client is None:
    print("CAN NOT CONNECT TO MONGODB")
    


app.include_router(news_controller.router)