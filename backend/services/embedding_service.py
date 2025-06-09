import math 
from typing import List,  Dict
from models.batch_term import BatchTerm
from models.term import TermFrequency
import numpy as np

def compute_tf(doc_tokens):
    tf = {}
    for word in doc_tokens:
        tf[word] = tf.get(word, 0) + 1
    for word in tf:
        tf[word] /= len(doc_tokens)
    return tf

def tf_map_to_term_frequency(tf_map: Dict[str, float]) -> List[TermFrequency]:
    """
    Chuyển đổi một map tần suất từ thành list các đối tượng TermFrequency.

    Args:
        tf_map (Dict[str, int]): Một dictionary với key là tên từ (str)
                                 và value là tần suất (int).

    Returns:
        List[TermFrequency]: Một list chứa các đối tượng TermFrequency.
    """
    return [
        TermFrequency(term_name=key, frequency=value) # Hoặc TermFrequency(**{"term_name": key, "frequency": value})
        for key, value in tf_map.items()
    ]


def compute_idf(docs):
    """
    Tính toán IDF và các thông tin liên quan cho một tập hợp các tài liệu.

    Args:
        docs (list of list of str): Một danh sách các tài liệu,
                                    mỗi tài liệu là một danh sách các từ.

    Returns:
        tuple: Một tuple chứa:
               - idf (dict): Một dictionary ánh xạ từ sang giá trị IDF của nó.
               - word2idx (dict): Một dictionary ánh xạ từ sang chỉ mục của nó.
               - ds_posting (dict): Một dictionary ánh xạ từ sang một map
                                    chứa 'count' (tần suất xuất hiện trong tài liệu)
                                    và 'related_docs' (tập hợp các chỉ mục tài liệu).
    """
    N = len(docs)
    ds_posting = {} 
    for doc_idx, doc in enumerate(docs):
        unique_words = set(doc) 
        for word in unique_words:
            if word not in ds_posting:
                ds_posting[word] = {'count': 0, 'related_docs': []}
            
            ds_posting[word]['count'] += 1
            ds_posting[word]['related_docs'].append(doc_idx)

    idf = {}
    word2idx = {}

    sorted_words = sorted(ds_posting.keys())

    for idx, word in enumerate(sorted_words):
        # Tính toán IDF sử dụng công thức với smooth factor (+1)
        # N: tổng số tài liệu
        # ds_posting[word]['count']: số tài liệu chứa từ 'word'
        idf[word] = math.log((N + 1) / (ds_posting[word]['count'] + 1)) + 1
        word2idx[word] = idx

    return idf, word2idx, ds_posting

    
def compute_tfidf_vector(doc_tokens, word2idx, idf):
    tf = compute_tf(doc_tokens)
    vector = [0] * len(idf)
    for word in tf:
        idx = word2idx[word]
        vector[idx] = tf[word] * idf[word]
    return vector

# def calculate_term_quantity(list_tokens: List[str]):
    
def compute_idf_batch(batch_terms: List[BatchTerm], all_docs_quantity: int) -> List[BatchTerm]:
    for term_data in batch_terms:
        # Tính toán IDF sử dụng công thức với smooth factor (+1)
        # N: tổng số tài liệu
        # ds_posting[word]['count']: số tài liệu chứa từ 'word'
        term_data["idf"] = math.log((all_docs_quantity + 1) / (term_data["count_docs"] + 1)) + 1
    return batch_terms

def compute_tfidf_vector_batch(term_frequence: List[TermFrequency], batch_terms_map, vector_len):
    vector = [0] * vector_len
    for term in term_frequence:
        term_name = term.term_name
        term_freq = term.frequency
        if not term_name or term_freq is None:
            # Có thể log lỗi hoặc bỏ qua nếu dữ liệu không hợp lệ
            continue
        if term_name in batch_terms_map:
            term_info = batch_terms_map[term_name]
            idx = term_info.get("idx")
            idf = term_info.get("idf")
            if idx is not None and idf is not None and isinstance(idx, int) and 0 <= idx < vector_len:
                vector[idx] = term_freq * idf
    return vector


def compute_bm25_vector_batch(term_frequence: List[TermFrequency], doc_len: int, batch_terms_map, vector_len, b, k, avgdl):
    vector = [0] * vector_len
    for term in term_frequence:
        term_name = term.term_name
        term_freq = term.frequency
        if not term_name or term_freq is None:
            # Có thể log lỗi hoặc bỏ qua nếu dữ liệu không hợp lệ
            continue
        if term_name in batch_terms_map:
            term_info = batch_terms_map[term_name]
            
            idx = term_info.get("idx")
            idf = term_info.get("idf")
            if idx is not None and idf is not None and isinstance(idx, int) and 0 <= idx < vector_len:
                vector[idx] = idf * ((term_freq * (k + 1)) / (term_freq + k * (1 - b + b * (doc_len / avgdl))))
    return vector

def normalize_vector(vector: list[float], norm_type: str = "l2") -> List[float]:
    """
    Chuẩn hóa các thành phần trong một vector.

    Args:
        vector (list[float]): Danh sách các giá trị số (vector) cần chuẩn hóa.
        norm_type (str): Loại chuẩn hóa muốn sử dụng.
                         - "l1" (hoặc "manhattan"): Chuẩn hóa L1.
                         - "l2" (hoặc "euclidean"): Chuẩn hóa L2 (mặc định).

    Returns:
        list[float]: Vector đã được chuẩn hóa.
                     Trả về vector gốc nếu nó là vector 0 (để tránh chia cho 0).
    """
    np_vector = np.array(vector, dtype=np.float32)

    if norm_type.lower() == "l1" or norm_type.lower() == "manhattan":
        norm_value = np.sum(np.abs(np_vector))
    elif norm_type.lower() == "l2" or norm_type.lower() == "euclidean":
        norm_value = np.linalg.norm(np_vector) 
    else:
        raise ValueError("Loại chuẩn hóa không hợp lệ. Chỉ chấp nhận 'l1' hoặc 'l2'.")

    if norm_value == 0:
        return vector 

    normalized_np_vector = np_vector / norm_value

    return normalized_np_vector.tolist()
