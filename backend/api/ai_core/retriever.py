# retrieval_service.py with caching

import redis
import json
import hashlib
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings


class RetrievalService:
    def __init__(
        self,
        qdrant_url,
        qdrant_api_key,
        collection_name,
        redis_host="127.0.0.1",
        redis_port=6379,
        redis_password="",
        cache_ttl=3600,
        embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):
        """Initialize the retrieval service with vector store and caching.
        
        Args:
            qdrant_url: URL for the Qdrant vector database
            qdrant_api_key: API key for Qdrant access
            collection_name: Name of the collection to search in
            redis_host: Redis host for caching
            redis_port: Redis port
            redis_password: Redis password
            cache_ttl: Cache time-to-live in seconds
            embedding_model_name: Name of the HuggingFace embedding model to use
        """
        # Initialize Redis cache
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True
        )
        
        # Cache TTL in seconds
        self.cache_ttl = cache_ttl
        
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
        
        # Initialize embedding model
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
        
        # Initialize vector store
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=self.embedding_model,
            content_payload_key="page_content",
            metadata_payload_key="metadata",
            vector_name="fast-all-minilm-l6-v2",
        )

    def vectorstore_backed_retriever(self, article_id, search_type="similarity", k=4, score_threshold=None):
        """Create a vectorsore-backed retriever.
        
        Args:
            article_id: ID of the article to search for
            search_type: Type of search - "similarity" (default), "mmr", or "similarity_score_threshold"
            k: Number of documents to return (Default: 4)
            score_threshold: Minimum relevance threshold for similarity_score_threshold (default=None)
            
        Returns:
            The retriever object
        """
        search_kwargs = {}
        if k is not None:
            search_kwargs['k'] = k
        if score_threshold is not None:
            search_kwargs['score_threshold'] = score_threshold
        
        metadata_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="original_id",
                    match=models.MatchValue(value=article_id)
                )
            ]
        )
        search_kwargs["filter"] = metadata_filter
        
        retriever = self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
        return retriever

    def _generate_cache_key(self, article_id):
        """Generate a deterministic cache key from request parameters.
        
        Args:
            article_id: ID of the article
            
        Returns:
            Cache key string
        """
        key_string = f"article:{article_id}"
        # Create a hash to keep the key size manageable
        return f"retrieval:{hashlib.md5(key_string.encode()).hexdigest()}"

    def retrieve_documents(self, request):
        """Retrieve documents for a given article ID, with caching.
        
        Args:
            request: RetrievalRequest object with article_id
            
        Returns:
            RetrievalResponse object with chunks and cache_hit status
        """
        try:
            # Generate cache key
            cache_key = self._generate_cache_key(request.article_id)
            
            # Try to get from cache first
            cached_result = self.redis_client.get(cache_key)
            if cached_result:
                chunks = json.loads(cached_result)
                return chunks #RetrievalResponse(chunks=chunks, cache_hit=True)
            
            # Get retriever and search
            retriever = self.vectorstore_backed_retriever(
                int(request.article_id),
                search_type="similarity", 
                k=4, 
                score_threshold=None
            )
            
            results = retriever.invoke(request.query)

            
            # Format results
            chunks = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                } for doc in results
            ]
            
            # Cache the results
            self.redis_client.setex(
                cache_key,
                self.cache_ttl,
                json.dumps(chunks)
            )

            
            return chunks #RetrievalResponse(chunks=chunks, cache_hit=False)
            
        except Exception as e:
            # Return the error
            raise Exception(f"Error in document retrieval: {str(e)}")

    def invalidate_cache(self, article_id):
        """Invalidate all cached results for a specific article.
        
        Args:
            article_id: ID of the article to invalidate cache for
            
        Returns:
            Dictionary with message about invalidated entries
        """
        pattern = f"retrieval:*article:{article_id}*"
        keys_to_delete = []
        
        # Scan for matching keys
        cursor = 0
        while True:
            cursor, keys = self.redis_client.scan(cursor, pattern, 100)
            keys_to_delete.extend(keys)
            if cursor == 0:
                break
        
        # Delete the keys
        if keys_to_delete:
            self.redis_client.delete(*keys_to_delete)
        
        return {"message": f"Invalidated {len(keys_to_delete)} cache entries for article {article_id}"}

    def get_stats(self):
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        # Get hit and miss values, defaulting to avoid division by zero
        hits = self.redis_client.info().get("keyspace_hits", 0)
        misses = self.redis_client.info().get("keyspace_misses", 1)
        
        cache_info = {
            "cache_size": self.redis_client.dbsize(),
            "cache_hit_rate": (hits / (hits + misses)) * 100 if (hits + misses) > 0 else 0,
            "uptime_seconds": self.redis_client.info().get("uptime_in_seconds", 0)
        }
        return cache_info