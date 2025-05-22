import os
from dotenv import load_dotenv
from api.ai_core.agent import ChatbotService
from api.ai_core.postsearch import TextSearcher, NeuralSearcher
from api.ai_core.config import COLLECTION_NAME

load_dotenv()

# Initialize services
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


def chat(user_id: str, article_id: str, query: str):
    response = chatbot.chat(user_id, article_id, query)
    return response["answer"], response["chat_history"]


def reset_conversation(user_id: str, article_id: str):
    chatbot.reset_conversation(user_id, article_id)
