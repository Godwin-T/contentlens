# api/v1/services/ai_service.py
from api.ai_core.neural_searcher import NeuralSearcher
from api.ai_core.text_searcher import TextSearcher
from api.ai_core.retriever import RetrievalService
from api.ai_core.chat_helper import ChatbotService
from api.ai_core.config import COLLECTION_NAME, QDRANT_API_KEY, QDRANT_URL
from api.v1.schemas.blog import RetrievalRequest
from langchain.schema import Document
from typing import List


# Initialize services
neural_searcher = NeuralSearcher(collection_name=COLLECTION_NAME)
text_searcher = TextSearcher(collection_name=COLLECTION_NAME)
retriever = RetrievalService(
    qdrant_url=QDRANT_URL,
    qdrant_api_key=QDRANT_API_KEY,
    collection_name=COLLECTION_NAME,
)
chatbot = ChatbotService(retriever, redis_url="redis://127.0.0.1:6379")


def read_item(q: str, neural: bool = True):
    return {
        "result": neural_searcher.search(text=q)
        if neural
        else text_searcher.search(query=q)
    }


def retrieve_documents(request: RetrievalRequest):
    try:
        return retriever.retrieve_documents(request)
    except Exception as e:
        raise Exception(f"Error retrieving documents: {str(e)}")


def invalidate_retrieval_cache(article_id: str):
    return retriever.invalidate_cache(article_id)


def get_retrieval_stats():
    return retriever.get_stats()


def chat(user_id: str, article_id: str, query: str):
    response = chatbot.chat(user_id, article_id, query)
    return response["answer"], response["chat_history"]


def reset_conversation(user_id: str, article_id: str):
    chatbot.reset_conversation(user_id, article_id)
