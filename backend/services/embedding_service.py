import math 

def compute_tf(doc_tokens):
    tf = {}
    for word in doc_tokens:
        tf[word] = tf.get(word, 0) + 1
    for word in tf:
        tf[word] /= len(doc_tokens)
    return tf

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