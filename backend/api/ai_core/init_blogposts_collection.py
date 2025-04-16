import os.path
from qdrant_client import QdrantClient, models
from tqdm import tqdm
from api.v1.services.blog_service import get_all_posts
from api.ai_core.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    COLLECTION_NAME,
    EMBEDDINGS_MODEL,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter


def upload_or_update_embeddings():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    client.set_model(EMBEDDINGS_MODEL)

    # Check if collection exists
    collections = client.get_collections()
    collection_exists = any(
        collection.name == COLLECTION_NAME for collection in collections.collections
    )

    # Get blog posts
    blogposts = get_all_posts()

    # Initialize text splitter for chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Characters per chunk
        chunk_overlap=100,  # Overlap between chunks
        separators=[
            "\n\n",
            "\n",
            " ",
            "",
        ],  # Split by paragraphs, then lines, then words
    )

    # Process each blog post and chunk it
    all_chunks = []
    all_metadata = []
    all_ids = []

    chunk_id = 0  # Global counter for unique chunk IDs
    for post in blogposts:
        # Split the content into chunks
        chunks = text_splitter.split_text(post.content)

        # Create metadata for each chunk
        for i, chunk in enumerate(chunks):
            chunk_id += 1
            all_chunks.append(chunk)
            all_metadata.append(
                {
                    "original_id": post.id,
                    "title": post.title,
                    "chunk_index": i,
                    "chunk_count": len(chunks),
                    # Store the chunk text in page_content for LangChain compatibility
                    "page_content": chunk,
                }
            )
            all_ids.append(chunk_id)  # Use a unique ID for each chunk

    if not collection_exists:
        # Create new collection if it doesn't exist
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=client.get_fastembed_vector_params(on_disk=True),
            quantization_config=models.ScalarQuantization(
                scalar=models.ScalarQuantizationConfig(
                    type=models.ScalarType.INT8, quantile=0.99, always_ram=True
                )
            ),
        )

        # Create payload index for page_content field (LangChain compatibility)
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="page_content",  # Use page_content for LangChain
            field_schema=models.TextIndexParams(
                type=models.TextIndexType.TEXT,
                tokenizer=models.TokenizerType.WORD,
                min_token_len=2,
                max_token_len=20,
                lowercase=True,
            ),
        )

        # Add all records
        client.add(
            collection_name=COLLECTION_NAME,
            documents=all_chunks,  # Use chunked content
            metadata=all_metadata,
            ids=tqdm(all_ids),
            parallel=6,
        )
        print(
            f"Created collection {COLLECTION_NAME} with {len(all_chunks)} chunked records"
        )
    else:
        # Collection exists, so we need to update
        # Get existing points to determine what's new and what needs updating
        try:
            existing_ids = set(
                p.id
                for p in client.scroll(
                    collection_name=COLLECTION_NAME,
                    limit=100000,  # Adjust based on your expected data size
                )[0]
            )
        except Exception as e:
            print(f"Error retrieving existing records: {e}")
            existing_ids = set()

        # Split data into new records and updates
        new_indices = []

        for idx, id_val in enumerate(all_ids):
            if id_val not in existing_ids:
                new_indices.append(idx)

        # Add new records
        if new_indices:
            new_chunks = [all_chunks[i] for i in new_indices]
            new_metadata = [all_metadata[i] for i in new_indices]
            new_ids = [all_ids[i] for i in new_indices]

            client.add(
                collection_name=COLLECTION_NAME,
                documents=new_chunks,
                metadata=new_metadata,
                ids=tqdm(new_ids),
                parallel=6,
            )
            print(
                f"Added {len(new_indices)} new chunked records to collection {COLLECTION_NAME}"
            )
        else:
            print("No changes made")


def use_with_langchain():
    """Example of how to use the created collection with LangChain"""
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_qdrant import QdrantVectorStore

    # Initialize the embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Connect to Qdrant
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    # Create the vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embedding_model,
        content_payload_key="page_content",  # Use the field we stored our text in
    )

    # Example search
    query = "What is machine learning?"
    docs = vector_store.similarity_search(query, k=4)

    # Print results
    for i, doc in enumerate(docs):
        print(f"Document {i+1}:\n{doc.page_content}\n{'-' * 50}")

    return vector_store


if __name__ == "__main__":
    upload_or_update_embeddings()
    # Uncomment to test with LangChain immediately
    # vector_store = use_with_langchain()
