from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
from dotenv import load_dotenv
from services import database
from controllers import news_controller, query_controller
from fastapi.middleware.cors import CORSMiddleware
# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Quản lý lifecycle của ứng dụng - startup và shutdown"""
    # Startup logic
    try:
        logger.info("Starting application...")
        
        # Kết nối MongoDB
        logger.info("Connecting to MongoDB...")
        database.connect_to_mongodb()
        
        if database.client is None:
            logger.error("Cannot connect to MongoDB")
            raise Exception("Failed to connect to MongoDB")
        
        logger.info("MongoDB connection established successfully")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        if database.client:
            try:
                database.client.close()
            except:
                pass
        raise e
    
    yield
    
    # Shutdown logic
    logger.info("Shutting down application...")
    try:
        if database.client:
            database.client.close()
            logger.info("MongoDB connection closed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Khởi tạo FastAPI app
app = FastAPI(
    title="Search Engine API",
    description="API cho hệ thống tìm kiếm tin tức",
    version="1.0.0",
    lifespan=lifespan
)

# Cho phép tất cả origins - chỉ dùng development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi domain/IP
    allow_credentials=False,  # Phải False khi dùng "*"
    allow_methods=["*"],
    allow_headers=["*"],
)


# API test đơn giản
@app.get("/")
async def test_api():
    """Endpoint test cơ bản"""
    return {
        "message": "Cảm ơn bạn đã sử dụng search engine của chúng tôi!",
        "version": "1.0.0"
    }

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Xử lý HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Xử lý tất cả exceptions khác"""
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

# Include routers
app.include_router(news_controller.router, prefix="/api/v1", tags=["News"])
app.include_router(query_controller.router, prefix="/api/v1", tags=["Search"])
