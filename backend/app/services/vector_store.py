from opensearchpy import OpenSearch, RequestsHttpConnection
from typing import List, Dict, Any
import numpy as np
from ..core.config import settings

class VectorStore:
    def __init__(self):
        self.client = OpenSearch(
            hosts=[{'host': settings.OPENSEARCH_HOST, 'port': settings.OPENSEARCH_PORT}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
            connection_class=RequestsHttpConnection
        )
        self.index_name = "interview_data"
        self._create_index_if_not_exists()
    
    def _create_index_if_not_exists(self):
        """Create the OpenSearch index if it doesn't exist"""
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(
                index=self.index_name,
                body={
                    "settings": {
                        "index": {
                            "knn": True
                        }
                    },
                    "mappings": {
                        "properties": {
                            "text": {"type": "text"},
                            "embedding": {
                                "type": "knn_vector",
                                "dimension": 1536  # OpenAI embedding dimension
                            },
                            "metadata": {
                                "properties": {
                                    "source": {"type": "keyword"},
                                    "type": {"type": "keyword"},
                                    "timestamp": {"type": "date"}
                                }
                            }
                        }
                    }
                }
            )
    
    def add_document(self, text: str, embedding: List[float], metadata: Dict[str, Any]):
        """Add a document to the vector store"""
        document = {
            "text": text,
            "embedding": embedding,
            "metadata": metadata
        }
        self.client.index(
            index=self.index_name,
            body=document,
            refresh=True
        )
    
    def search_similar(self, query_embedding: List[float], k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity"""
        query = {
            "size": k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_embedding,
                        "k": k
                    }
                }
            }
        }
        
        response = self.client.search(
            index=self.index_name,
            body=query
        )
        
        results = []
        for hit in response["hits"]["hits"]:
            results.append({
                "text": hit["_source"]["text"],
                "metadata": hit["_source"]["metadata"],
                "score": hit["_score"]
            })
        
        return results
    
    def get_candidate_history(self, candidate_id: str, k: int = 5) -> List[Dict[str, Any]]:
        """Get similar candidate interview history"""
        query = {
            "size": k,
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "metadata.type": "interview"
                            }
                        },
                        {
                            "term": {
                                "metadata.candidate_id": candidate_id
                            }
                        }
                    ]
                }
            },
            "sort": [
                {
                    "metadata.timestamp": {
                        "order": "desc"
                    }
                }
            ]
        }
        
        response = self.client.search(
            index=self.index_name,
            body=query
        )
        
        results = []
        for hit in response["hits"]["hits"]:
            results.append({
                "text": hit["_source"]["text"],
                "metadata": hit["_source"]["metadata"],
                "score": hit["_score"]
            })
        
        return results 