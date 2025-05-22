import os
import re
import time
import opik
from typing import List

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models.models import Filter, FieldCondition, MatchText
from api.ai_core.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    EMBEDDINGS_MODEL,
    TEXT_FIELD_NAME,
)


load_dotenv()
os.environ["OPIK_API_KEY"] = os.getenv("OPIK_API_KEY")
os.environ["OPIK_WORKSPACE"] = os.getenv("OPIK_WORKSPACE")
os.environ["OPIK_PROJECT_NAME"] = os.getenv("OPIK_PROJECT_NAME")


class NeuralSearcher:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True
        )
        self.qdrant_client.set_model(EMBEDDINGS_MODEL)

    @opik.track(capture_input=True, capture_output=True)
    def search(self, text: str, filter_: dict = None) -> List[dict]:
        start_time = time.time()
        hits = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            query_filter=Filter(**filter_) if filter_ else None,
            limit=5,
        )
        print(f"Search took {time.time() - start_time} seconds")
        return [hit.metadata for hit in hits]


class TextSearcher:
    def __init__(self, collection_name: str):
        self.highlight_field = TEXT_FIELD_NAME
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True
        )

    def highlight(self, record, query) -> dict:
        text = record[self.highlight_field]

        for word in query.lower().split():
            if len(word) > 4:
                pattern = re.compile(
                    rf"(\b{re.escape(word)}?.?\b)", flags=re.IGNORECASE
                )
            else:
                pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
            text = re.sub(pattern, r"<b>\1</b>", text)

        record[self.highlight_field] = text
        return record

    def search(self, query, top=5):
        hits = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key=TEXT_FIELD_NAME,
                        match=MatchText(text=query),
                    )
                ]
            ),
            with_payload=True,
            with_vectors=False,
            limit=top,
        )
        return [self.highlight(hit.payload, query) for hit in hits[0]]
