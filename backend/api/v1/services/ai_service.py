import os
from dotenv import load_dotenv
from api.v1.schemas.blog import RetrievalRequest
from api.ai_core.agent import RetrievalService, ChatbotService
from api.ai_core.postsearch import TextSearcher, NeuralSearcher
from api.ai_core.config import COLLECTION_NAME, QDRANT_API_KEY, QDRANT_URL

load_dotenv()

# Initialize services

# retriever = RetrievalService(
#     qdrant_url=QDRANT_URL,
#     qdrant_api_key=QDRANT_API_KEY,
#     collection_name=COLLECTION_NAME,
# )
redis_url = os.getenv("REDIS_URL")
chatbot = ChatbotService(redis_url=redis_url)
neural_searcher = NeuralSearcher(collection_name=COLLECTION_NAME)
text_searcher = TextSearcher(collection_name=COLLECTION_NAME)


def read_item(q: str, neural: bool = True):
    return {
        "result": neural_searcher.search(text=q)
        if neural
        else text_searcher.search(query=q)
    }


# def retrieve_documents(request: RetrievalRequest):
#     try:
#         return retriever.retrieve_documents(request)
#     except Exception as e:
#         raise Exception(f"Error retrieving documents: {str(e)}")


# def invalidate_retrieval_cache(article_id: str):
#     return retriever.invalidate_cache(article_id)


# def get_retrieval_stats():
#     return retriever.get_stats()


def chat(user_id: str, article_id: str, query: str):
    response = chatbot.chat(user_id, article_id, query)
    return response["answer"], response["chat_history"]


def reset_conversation(user_id: str, article_id: str):
    chatbot.reset_conversation(user_id, article_id)
