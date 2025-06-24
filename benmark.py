import numpy as np
import time

# --- Cấu hình kích thước và kiểu dữ liệu ---
VECTOR_DIM = 10000
MATRIX_ROWS = 10000
MATRIX_COLS = VECTOR_DIM # Kích thước cột của ma trận phải bằng kích thước vector

DTYPE = np.float32 # Chỉ sử dụng float32

print(f"--- Benchmarking Tích Ma trận-Vector (Matrix x Vector) với Vector {VECTOR_DIM} chiều và Ma trận {MATRIX_ROWS}x{MATRIX_COLS} (float32) ---")

# --- Khởi tạo dữ liệu (sử dụng float32) ---
print("\nKhởi tạo Ma trận và Vector...")
start_init_mat = time.time()
mat = np.random.rand(MATRIX_ROWS, MATRIX_COLS).astype(DTYPE)
end_init_mat = time.time()
print(f"  Ma trận khởi tạo trong: {end_init_mat - start_init_mat:.4f} giây")

start_init_vec = time.time()
vec = np.random.rand(VECTOR_DIM).astype(DTYPE)
end_init_vec = time.time()
print(f"  Vector khởi tạo trong: {end_init_vec - start_init_vec:.4f} giây")

# --- Ước tính Bộ nhớ Tiêu thụ (cho thông tin thêm) ---
print("\nƯớc tính Bộ nhớ Tiêu thụ:")
print(f"  Ma trận {MATRIX_ROWS}x{MATRIX_COLS} ({DTYPE.__name__}): {mat.nbytes / (1024**2):.2f} MB")
print(f"  Vector {VECTOR_DIM} ({DTYPE.__name__}): {vec.nbytes / (1024**2):.2f} MB")


# --- Thực hiện phép toán Tích Ma trận-Vector (Matrix x Vector) ---
# mat (20000x50000) . vec (50000x1) -> result (20000x1)
print("\nThực hiện phép toán Tích Ma trận-Vector...")
start_dot_product = time.time()
result = np.dot(mat, vec)
end_dot_product = time.time()
duration_dot_product = end_dot_product - start_dot_product

print(f"\nThời gian thực hiện Tích Ma trận-Vector ({DTYPE.__name__}): {duration_dot_product:.4f} giây")

# Kiểm tra hình dạng của kết quả (sẽ là (MATRIX_ROWS,))
print(f"Hình dạng của vector kết quả: {result.shape}")