from typing import List
import numpy as np
import heapq

async def dot_product(query: List[float], list_docs: List[List[float]]) -> np.ndarray:
    """
    Tính tích vô hướng của một vector truy vấn với từng vector trong danh sách các vector tài liệu.

    Args:
        query (List[float]): Vector truy vấn.
        list_docs (List[List[float]]): Danh sách các vector tài liệu.

    Returns:
        np.ndarray: Một mảng NumPy chứa giá trị tích vô hướng của query với mỗi vector trong list_docs.
                    Thứ tự các giá trị tương ứng với thứ tự các vector trong list_docs.
    """
    if not query or not list_docs:
        return np.array([]) 

    np_query = np.array(query)
    np_docs = np.array(list_docs) 

   
    if np_query.ndim != 1:
        raise ValueError("Vector truy vấn phải là một vector 1 chiều.")
    if np_docs.ndim != 2:
        raise ValueError("Danh sách tài liệu phải là mảng 2 chiều (mỗi hàng là một vector tài liệu).")
    if np_query.shape[0] != np_docs.shape[1]:
        raise ValueError(
            f"Kích thước vector không khớp. Query có {np_query.shape[0]} phần tử, "
            f"trong khi các vector tài liệu có {np_docs.shape[1]} phần tử."
        )

    dot_products_array = np.dot(np_docs, np_query)

    return dot_products_array



def get_n_largest_indices_and_values(distances, n):
    """
    Lấy ra n chỉ mục và giá trị lớn nhất từ một danh sách các khoảng cách.
    Sử dụng heapq để tối ưu hiệu suất.
    """
    if not isinstance(distances, list) or not distances or n <= 0:
        return []
    top_n = heapq.nlargest(n, enumerate(distances), key=lambda x: x[1])
    # Đổi vị trí tuple thành (giá trị, chỉ mục) 
    return [(value, index) for index, value in top_n]