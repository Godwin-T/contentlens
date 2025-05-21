# retrieval_service.py with caching

import os
import json
import opik
import redis
import hashlib

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from api.ai_core.prompt import create_answer_prompt, create_standalone_question_prompt
from api.ai_core.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME


load_dotenv()
os.environ["OPIK_API_KEY"] = os.getenv("OPIK_API_KEY")
os.environ["OPIK_WORKSPACE"] = os.getenv("OPIK_WORKSPACE")
os.environ["OPIK_PROJECT_NAME"] = os.getenv("OPIK_PROJECT_NAME")


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
        embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
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
            decode_responses=True,
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

    @opik.track(capture_input=True, capture_output=True)
    def vectorstore_backed_retriever(
        self, article_id, search_type="similarity", k=4, score_threshold=None
    ):
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
            search_kwargs["k"] = k
        if score_threshold is not None:
            search_kwargs["score_threshold"] = score_threshold

        metadata_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="original_id", match=models.MatchValue(value=article_id)
                )
            ]
        )
        search_kwargs["filter"] = metadata_filter

        retriever = self.vector_store.as_retriever(
            search_type=search_type, search_kwargs=search_kwargs
        )
        return retriever

    @opik.track(capture_input=False, capture_output=False)
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

    @opik.track(capture_input=True, capture_output=True)
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
                return chunks  # RetrievalResponse(chunks=chunks, cache_hit=True)

            # Get retriever and search
            retriever = self.vectorstore_backed_retriever(
                int(request.article_id),
                search_type="similarity",
                k=4,
                score_threshold=None,
            )

            results = retriever.invoke(request.query)

            # Format results
            chunks = [
                {"content": doc.page_content, "metadata": doc.metadata}
                for doc in results
            ]

            # Cache the results
            self.redis_client.setex(cache_key, self.cache_ttl, json.dumps(chunks))

            return chunks  # RetrievalResponse(chunks=chunks, cache_hit=False)

        except Exception as e:
            # Return the error
            raise Exception(f"Error in document retrieval: {str(e)}")

    @opik.track(capture_input=True, capture_output=True)
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

        return {
            "message": f"Invalidated {len(keys_to_delete)} cache entries for article {article_id}"
        }

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
            "cache_hit_rate": (hits / (hits + misses)) * 100
            if (hits + misses) > 0
            else 0,
            "uptime_seconds": self.redis_client.info().get("uptime_in_seconds", 0),
        }
        return cache_info


class ConversationalRetrievalBot:
    """
    A class for creating and managing conversational retrieval chains for multiple users.
    """

    def __init__(
        self,
        redis_url="http://127.0.0.1:6379",
        google_api_key=None,
        model="gemini-2.0-flash-lite",
        temperature=0.5,
        top_p=0.9,
    ):
        """
        Initialize the bot with configuration parameters.

        Args:
            redis_url (str, optional): Redis URL for chat history persistence. Defaults to environment variable.
            google_api_key (str, optional): Google API key. Defaults to environment variable.
            model (str, optional): Model name for Google Generative AI. Defaults to "gemini-2.0-flash-lite".
            temperature (float, optional): Temperature parameter for generation. Defaults to 0.5.
            top_p (float, optional): Top-p parameter for generation. Defaults to 0.9.
        """
        # Load environment variables if not explicitly provided
        load_dotenv()

        # Set API keys
        self.google_api_key = google_api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("Google API key is required")

        self.redis_url = redis_url  # or os.environ.get("REDIS_URL")
        if not self.redis_url:
            raise ValueError("Redis URL is required for persistent chat history")

        # Create LLM instance
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=self.google_api_key,
            model=model,
            temperature=temperature,
            top_p=top_p,
            # convert_system_message_to_human=True
        )

        # Use the same LLM for question condensation
        self.condense_question_llm = self.llm

        # Store user chains
        self.user_chains = {}

        # During development - use prompts without versioning
        self.answer_prompt = create_answer_prompt(language="english")
        self.standalone_question_prompt = create_standalone_question_prompt()

    @opik.track(capture_input=False, capture_output=False)
    def _create_memory(self, session_id):
        """
        Create memory specific to a user session.

        Args:
            session_id (str): Unique identifier for the user session.

        Returns:
            ConversationBufferMemory: Memory instance for the specified session.
        """
        message_history = RedisChatMessageHistory(
            session_id=session_id, url=self.redis_url
        )
        memory = ConversationBufferMemory(
            chat_memory=message_history,
            return_messages=True,
            memory_key="chat_history",
            output_key="answer",
            input_key="question",
        )
        return memory

    @opik.track(capture_input=True, capture_output=True)
    def get_chain_for_user(self, session_id, retriever, language="english"):
        """
        Get or create a conversational chain for a specific user.

        Args:
            session_id (str): Unique identifier for the user session.
            retriever: Document retriever instance.
            language (str, optional): Language for responses. Defaults to "english".

        Returns:
            ConversationalRetrievalChain: Chain for the specified user.
        """
        # Return existing chain if already created
        if session_id in self.user_chains:
            return self.user_chains[session_id]

        # Create user-specific memory
        memory = self._create_memory(session_id)

        # Create the chain
        chain = ConversationalRetrievalChain.from_llm(
            condense_question_prompt=self.standalone_question_prompt,
            combine_docs_chain_kwargs={"prompt": self.answer_prompt},
            condense_question_llm=self.condense_question_llm,
            memory=memory,
            retriever=retriever,
            llm=self.llm,
            chain_type="stuff",
            verbose=False,
            return_source_documents=True,
        )

        # Store chain for future use
        self.user_chains[session_id] = chain

        return chain

    @opik.track(capture_input=True, capture_output=True)
    def process_query(self, session_id, question, retriever, language="english"):
        """
        Process a user query and return the response.

        Args:
            session_id (str): Unique identifier for the user session.
            question (str): User's question.
            retriever: Document retriever instance.
            language (str, optional): Language for the response. Defaults to "english".

        Returns:
            dict: Response containing the answer and source documents.
        """
        chain = self.get_chain_for_user(session_id, retriever, language)
        return chain.invoke({"question": question})

    @opik.track(capture_input=True, capture_output=False)
    def clear_user_history(self, session_id):
        """
        Clear conversation history for a specific user.

        Args:
            session_id (str): Unique identifier for the user session.
        """
        if session_id in self.user_chains:
            # Remove from cache
            del self.user_chains[session_id]

        # Create and immediately clear Redis history
        message_history = RedisChatMessageHistory(
            session_id=session_id, url=self.redis_url
        )
        message_history.clear()


class ChatbotService:
    """
    Service class that uses the ConversationalRetrievalBot to provide chatbot functionality.
    """

    def __init__(self, redis_url=None):
        """
        Initialize the chatbot service.

        Args:
            redis_url (str, optional): Redis URL for chat history persistence.
        """
        # Initialize the conversational bot
        self.bot = ConversationalRetrievalBot(redis_url=redis_url)
        self.retriever = RetrievalService(
            qdrant_url=QDRANT_URL,
            qdrant_api_key=QDRANT_API_KEY,
            collection_name=COLLECTION_NAME,
        )

    @opik.track(capture_input=True, capture_output=True)
    def chat(
        self, user_id: str, article_id: str, message: str, language: str = "english"
    ):
        """
        Process a user message and return the chatbot's response.

        Args:
            user_id (str): Unique identifier for the user.
            article_id (str): ID of the article to search within.
            message (str): User's message.
            language (str, optional): Language for the response. Defaults to "english".

        Returns:
            dict: Chatbot's response containing the answer and source documents.
        """
        # Create a session ID that includes both user ID and article ID
        # This ensures separate conversation history for each user-article pair
        session_id = f"{user_id}:{article_id}"
        adapted_retriever = self.retriever.vectorstore_backed_retriever(int(article_id))

        # Process the query
        response = self.bot.process_query(
            session_id=session_id,
            question=message,
            retriever=adapted_retriever,
            language=language,
        )
        chain = self.bot.get_chain_for_user(session_id, adapted_retriever, language)
        chat_history = (
            chain.memory.chat_memory.messages if hasattr(chain, "memory") else []
        )

        # Process the chat history to a more usable format
        processed_history = []
        for msg in chat_history:
            # Convert LangChain message objects to a simpler dict format
            # Typically messages have a 'type' (human/ai) and 'content'
            msg_type = "user" if msg.type == "human" else "assistant"
            processed_history.append({"role": msg_type, "content": msg.content})

        # Return the full response including answer and source documents
        return {"answer": response["answer"], "chat_history": processed_history}

    @opik.track(capture_input=True, capture_output=False)
    def reset_conversation(self, user_id: str, article_id: str):
        """
        Reset the conversation history for a user-article pair.

        Args:
            user_id (str): Unique identifier for the user.
            article_id (str): ID of the article.
        """
        session_id = f"{user_id}:{article_id}"
        self.bot.clear_user_history(session_id)
