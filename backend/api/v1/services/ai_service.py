from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.ai_core.config import COLLECTION_NAME
from api.ai_core.text_searcher import TextSearcher
from api.ai_core.neural_searcher import NeuralSearcher

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

neural_searcher = NeuralSearcher(collection_name=COLLECTION_NAME)
text_searcher = TextSearcher(collection_name=COLLECTION_NAME)


def read_item(q: str, neural: bool = True):
    return {
        "result": neural_searcher.search(text=q)
        if neural
        else text_searcher.search(query=q)
    }
