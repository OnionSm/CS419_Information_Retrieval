from models.model_variable import ModelVariable
from services import model_variable_service

# Khai báo biến toàn cục và gán giá trị khởi tạo (thường là None hoặc giá trị mặc định)
model_variale: ModelVariable = None # Đây là khai báo global

async def load_global_variable():
    global model_variale # Khai báo rằng bạn muốn sử dụng biến `model_variale` toàn cục
    model_variale = await model_variable_service.get_model_variable() # Gán giá trị cho biến toàn cục