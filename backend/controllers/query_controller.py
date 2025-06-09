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
from models.query import QueryInput
from services import model_variable_service
from collections import Counter
from collections import defaultdict
import asyncio
import logging

# Cấu hình logger
logger = logging.getLogger(__name__)

# Sửa import này
from utils import vector_math  
import numpy as np


router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)

@router.post("/query", response_model=List[NewsRespone], status_code=status.HTTP_200_OK)
async def search(query_input: QueryInput) -> List[NewsRespone]:
    try:
        model_variable = await model_variable_service.get_model_variable()
        docs_quantity, terms_quantity, dict_len, k, b = (
            model_variable.docs_quantity,
            model_variable.terms_quantity, 
            model_variable.dict_len,
            model_variable.k,
            model_variable.b
        )

        query_input_dict = query_input.model_dump(by_alias=True, exclude_unset=True)
        query_input_dict["model"] = query_input_dict.get("model") or "tf-idf"
        query_input_dict["top_n"] = max(1, min(query_input_dict.get("top_n", 1), 99))
        

        tokens = text_preprocess.process_text(query_input.query)
        query_doc_size = len(tokens)
        
        # Get unique terms and related documents - optimized
        related_docs_map = {}
        set_terms = set(tokens)
        list_batch_term = []

        # Process all terms concurrently instead of sequentially
        
        term_tasks = [
            term_service.get_term_data_by_name_async(term_name) 
            for term_name in set_terms
        ]
        term_results = await asyncio.gather(*term_tasks, return_exceptions=True)

        # Process results efficiently
        for term_name, term_data in zip(set_terms, term_results):
            if isinstance(term_data, Exception) or not term_data:
                continue
            
            # Count related documents using get() method
            for doc_id in term_data.related_docs:
                related_docs_map[doc_id] = related_docs_map.get(doc_id, 0) + 1
            
            # Build batch term data directly
            list_batch_term.append({
                "id": term_data.id,
                "idx": term_data.idx,
                "term_name": term_data.term_name,
                "count_docs": term_data.count_rl_docs,
                "idf": 0
            })

        # Filter related documents (moved logic here for efficiency)
        related_docs = filter_related_docs_dynamic(related_docs_map, query_input_dict["top_n"])
        # print(len(related_docs))

        # Calculate IDF and prepare batch processing
        list_batch_term = embedding_service.compute_idf_batch(list_batch_term, docs_quantity)
        batch_terms_map = term_service.batch_terms_to_map(list_batch_term)

        # Query TF calculation
        query_tf = embedding_service.tf_map_to_term_frequency(
            embedding_service.compute_tf(tokens)
        )
        avgdl = terms_quantity / docs_quantity

        async def process_documents():
            # Fetch all documents concurrently
            doc_tasks = [news_service.get_news_by_id_async(doc_id) for doc_id in related_docs]
            docs = await asyncio.gather(*doc_tasks, return_exceptions=True)
            
            list_news = []
            list_vector_news = []
            
            for doc in docs:
                # Skip invalid documents or exceptions
                if isinstance(doc, Exception) or not doc or not getattr(doc, 'terms', None):
                    continue
                    
                list_news.append(doc)
                
                # Compute vector based on model type
                if query_input_dict["model"] == "tf-idf":
                    vector = embedding_service.compute_tfidf_vector_batch(
                        doc.terms, batch_terms_map, dict_len
                    )
                else:
                    vector = embedding_service.compute_bm25_vector_batch(
                        doc.terms, doc.doc_size, batch_terms_map, 
                        dict_len, b, k, avgdl
                    )
                
                list_vector_news.append(embedding_service.normalize_vector(vector))
            
            return list_news, list_vector_news

        # Execute concurrent processing
        list_news, list_vector_news = await process_documents()

        # Compute query vector based on model type
        if query_input_dict["model"] == "tf-idf":
            query_vector = embedding_service.compute_tfidf_vector_batch(
                query_tf, batch_terms_map, dict_len
            )            
        else:
            query_vector = embedding_service.compute_bm25_vector_batch(
                query_tf, query_doc_size, batch_terms_map, 
                dict_len, b, k, avgdl
            )

        query_vector = embedding_service.normalize_vector(query_vector)

        # Calculate similarities and get top results
        similarities = await vector_math.dot_product(query_vector, list_vector_news)
        list_top_n = vector_math.get_n_largest_indices_and_values(
            similarities.tolist(), query_input_dict["top_n"]
        )

        # Build response data efficiently
        res_data = [
            NewsRespone(
                title=list_news[index].title,
                description=list_news[index].description,
                content=list_news[index].content,
                link=list_news[index].link,
                score=score
            )
            for score, index in list_top_n
        ]

        return res_data
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi không mong muốn khi truy vấn: {e}"
        )


def filter_related_docs_dynamic(related_docs_map, top_n):
    threshold = 5
    while threshold >= 1:
        filtered_docs = {
            doc_id for doc_id, count in related_docs_map.items() 
            if count >= threshold
        }
        if len(filtered_docs) >= top_n:
            return filtered_docs
        threshold -= 1
    # Nếu không đủ, trả về tất cả documents
    return set(related_docs_map.keys())


@router.post("/hello", status_code=status.HTTP_200_OK)
async def hello():
    return {
        "message": "Hello User"
    }

@router.post("/test", status_code=status.HTTP_200_OK)
async def test_query(query_input: QueryInput):
    query_input = query_input.model_dump(by_alias=True, exclude_unset=True)
    return {
        "query": query_input["query"],
        "model": query_input["model"],
        "top_n": query_input["top_n"]
    }

