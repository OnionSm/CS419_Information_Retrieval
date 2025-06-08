from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from typing import List
from models.news import News
from pymongo.database import Database
from services import news_service, embedding_service
from models.news import News, NewsRespone
from services import text_preprocess
from services import term_service
from models.term import Term
from models.batch_term import BatchTerm
from backend import global_variable
from collections import Counter
from backend.utils import vector_math
import numpy as np

async def search(query: str, model: str, top_n: int) -> List[NewsRespone]:
    try:
        if global_variable.model_variale is None:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi không mong muốn khi truy vấn: {e}")
        
        # Preprocess query
        tokens = text_preprocess.process_text(query)
        query_doc_size = len(tokens)
        
        # Get unique term and related doc
        related_docs = set()
        set_terms = set(tokens)
        list_batch_term = []
        for term_name in set_terms:
            term_data = term_service.get_term_data_by_name_async(term_name)
            batch_term = {}
            if term_data: 
                related_docs.update(term_data["related_docs"])
                batch_term["id"] = term_data["id"]
                batch_term["count_docs"] = term_data["count_rl_docs"]
                batch_term["idf"] = 0
                list_batch_term.append(batch_term)


        # Calculate IDF for batch term
        list_batch_term = embedding_service.compute_idf_batch(list_batch_term, global_variable.model_variale["docs_quantity"])
        batch_terms_map = term_service.batch_terms_to_map(list_batch_term)


        # Query TF
        query_tf = embedding_service.compute_tf(tokens)
        query_tf = embedding_service.tf_map_to_term_frequency(query_tf)

        avgdl = global_variable.model_variale["terms_quantity"] / global_variable.model_variale["docs_quantity"]
        
        list_news = []
        list_vector_news = []
        # Get related docs 
        for doc_id in related_docs:
            doc = news_service.get_news_by_id_async(doc_id)
            if doc is not None and len(doc["terms"]) > 0:
                list_news.append(doc)
                if model == "tf-idf":
                    vector = embedding_service.compute_tfidf_vector_batch(doc["terms"], batch_terms_map, global_variable.model_variale["dict_len"])
                else:
                    
                    vector = embedding_service.compute_bm25_vector_batch(doc["terms"], doc["doc_size"], batch_terms_map, global_variable.model_variale["dict_len"], 
                                                            global_variable.model_variale["b"], global_variable.model_variale["k"], avgdl)
                vector = embedding_service.normalize_vector(vector)
                list_vector_news.append(vector)
        

        # Embedding query
        if model == "tf-idf":
            query_vector = embedding_service.compute_tfidf_vector_batch(query_tf, batch_terms_map, global_variable.model_variale["dict_len"])            
        else:
            query_vector = embedding_service.compute_bm25_vector_batch(query_tf, query_doc_size, batch_terms_map, global_variable.model_variale["dict_len"], 
                                                            global_variable.model_variale["b"], global_variable.model_variale["k"], avgdl)
        query_vector = embedding_service.normalize_vector(query_vector)

        # Dot product
        euclide_distance = vector_math.dot_product(query_vector, list_vector_news)
        list_top_n = vector_math.get_n_largest_indices_and_values(euclide_distance)

        res_data = []
        for top in list_top_n:
            score = top[0]
            index = top[1]
            raw_news = list_news[index]
            res_new = {}
            res_new["title"] = raw_news["title"]
            res_new["description"] = raw_news["description"]
            res_new["content"] = raw_news["content"]
            res_new["link"] = raw_news["link"]
            res_new["score"] = score
            res_data.append(NewsRespone(**res_new))
        
        return res_data
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi không mong muốn khi truy vấn: {e}")