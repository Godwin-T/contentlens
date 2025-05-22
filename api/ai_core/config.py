import os
from dotenv import load_dotenv

load_dotenv()

CODE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
STATIC_DIR = os.path.join(ROOT_DIR, "static")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333/")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "text-demo")
EMBEDDINGS_MODEL = os.getenv(
    "EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
)

TEXT_FIELD_NAME = "document"
