import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

client = None
db = None
def connect_to_mongodb():
    """
    Kết nối tới MongoDB bằng cách lấy cấu hình từ biến môi trường.

    Returns:
        MongoClient: Đối tượng client đã kết nối.
        Database: Đối tượng database đã chọn.
        None, None: Nếu kết nối hoặc xác thực thất bại.
    """
 
    MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
    MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
    MONGODB_HOST = os.environ.get("MONGODB_HOST") 
    MONGODB_PORT = int(os.environ.get("MONGODB_PORT"))
    MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE")
    AUTH_MECHANISM = os.environ.get("AUTH_MECHANISM")
    AUTH_SOURCE = os.environ.get("AUTH_SOURCE") 

    global client, db

    try:
        if MONGODB_USERNAME and MONGODB_PASSWORD:
            # Kết nối có xác thực
            client = MongoClient(
                host=MONGODB_HOST,
                port=MONGODB_PORT,
                username=MONGODB_USERNAME,
                password=MONGODB_PASSWORD,
                authSource=AUTH_SOURCE,
                authMechanism=AUTH_MECHANISM 
            )
     
        db = client[MONGODB_DATABASE]

    except ConnectionFailure as e:
        print(f"Lỗi kết nối MongoDB: Không thể kết nối tới server tại {MONGODB_HOST}:{MONGODB_PORT}. Chi tiết: {e}")
        return None, None
    except OperationFailure as e:
        print(f"Lỗi xác thực MongoDB: Vui lòng kiểm tra tên người dùng, mật khẩu và auth_source ('{AUTH_SOURCE}'). Chi tiết: {e}")
        return None, None
    except ValueError:
        print(f"Lỗi: PORT '{os.environ.get('MONGODB_PORT')}' không phải là số nguyên hợp lệ.")
        return None, None
    except Exception as e:
        print(f"Một lỗi không xác định đã xảy ra trong quá trình kết nối MongoDB: {e}")
        return None, None