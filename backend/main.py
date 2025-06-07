from fastapi import FastAPI, HTTPException, Depends
from typing import List
import os
import database
from controllers import news_controller
import global_variable
import asyncio

async def main():
    app = FastAPI()

    await database.connect_to_mongodb()

    if database.client is None:
        print("CAN NOT CONNECT TO MONGODB")
        
    await global_variable.load_global_variable()

    app.include_router(news_controller.router)

# Chạy hàm async chính
if __name__ == "__main__":
    asyncio.run(main())
    print("Script đã hoàn thành.")