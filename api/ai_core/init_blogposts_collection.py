# import os.path
# from qdrant_client import QdrantClient, models
# from tqdm import tqdm
# from api.v1.services.blog_service import get_all_posts
# from api.ai_core.config import (
#     QDRANT_URL,
#     QDRANT_API_KEY,
#     COLLECTION_NAME,
#     EMBEDDINGS_MODEL,
# )
# from langchain.text_splitter import RecursiveCharacterTextSplitter


# def upload_or_update_embeddings():
#     client = QdrantClient(
#         url=QDRANT_URL,
#         api_key=QDRANT_API_KEY,
#     )
#     client.set_model(EMBEDDINGS_MODEL)

#     # Check if collection exists
#     collections = client.get_collections()
#     collection_exists = any(
#         collection.name == COLLECTION_NAME for collection in collections.collections
#     )

#     # Get blog posts
#     blogposts = get_all_posts()

#     # Initialize text splitter for chunking
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,  # Characters per chunk
#         chunk_overlap=100,  # Overlap between chunks
#         separators=[
#             "\n\n",
#             "\n",
#             " ",
#             "",
#         ],  # Split by paragraphs, then lines, then words
#     )

#     # Process each blog post and chunk it
#     all_chunks = []
#     all_metadata = []
#     all_ids = []

#     chunk_id = 0  # Global counter for unique chunk IDs
#     for post in blogposts:
#         # Split the content into chunks
#         chunks = text_splitter.split_text(post.content)

#         # Create metadata for each chunk
#         for i, chunk in enumerate(chunks):
#             chunk_id += 1
#             all_chunks.append(chunk)
#             all_metadata.append(
#                 {
#                     "original_id": post.id,
#                     "title": post.title,
#                     "chunk_index": i,
#                     "chunk_count": len(chunks),
#                     # Store the chunk text in page_content for LangChain compatibility
#                     "page_content": chunk,
#                 }
#             )
#             all_ids.append(chunk_id)  # Use a unique ID for each chunk

#     if not collection_exists:
#         # Create new collection if it doesn't exist
#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=client.get_fastembed_vector_params(on_disk=True),
#             quantization_config=models.ScalarQuantization(
#                 scalar=models.ScalarQuantizationConfig(
#                     type=models.ScalarType.INT8, quantile=0.99, always_ram=True
#                 )
#             ),
#         )

#         # Create payload index for page_content field (LangChain compatibility)
#         client.create_payload_index(
#             collection_name=COLLECTION_NAME,
#             field_name="page_content",  # Use page_content for LangChain
#             field_schema=models.TextIndexParams(
#                 type=models.TextIndexType.TEXT,
#                 tokenizer=models.TokenizerType.WORD,
#                 min_token_len=2,
#                 max_token_len=20,
#                 lowercase=True,
#             ),
#         )

#         # Add all records
#         client.add(
#             collection_name=COLLECTION_NAME,
#             documents=all_chunks,  # Use chunked content
#             metadata=all_metadata,
#             ids=tqdm(all_ids),
#             parallel=6,
#         )
#         print(
#             f"Created collection {COLLECTION_NAME} with {len(all_chunks)} chunked records"
#         )
#     else:
#         # Collection exists, so we need to update
#         # Get existing points to determine what's new and what needs updating
#         try:
#             existing_ids = set(
#                 p.id
#                 for p in client.scroll(
#                     collection_name=COLLECTION_NAME,
#                     limit=100000,  # Adjust based on your expected data size
#                 )[0]
#             )
#         except Exception as e:
#             print(f"Error retrieving existing records: {e}")
#             existing_ids = set()

#         # Split data into new records and updates
#         new_indices = []

#         for idx, id_val in enumerate(all_ids):
#             if id_val not in existing_ids:
#                 new_indices.append(idx)

#         # Add new records
#         if new_indices:
#             new_chunks = [all_chunks[i] for i in new_indices]
#             new_metadata = [all_metadata[i] for i in new_indices]
#             new_ids = [all_ids[i] for i in new_indices]

#             client.add(
#                 collection_name=COLLECTION_NAME,
#                 documents=new_chunks,
#                 metadata=new_metadata,
#                 ids=tqdm(new_ids),
#                 parallel=6,
#             )
#             print(
#                 f"Added {len(new_indices)} new chunked records to collection {COLLECTION_NAME}"
#             )
#         else:
#             print("No changes made")

# if __name__ == "__main__":
#     upload_or_update_embeddings()


import os.path
import asyncio
from tqdm.asyncio import tqdm as async_tqdm 
from qdrant_client import QdrantClient, models
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from api.ai_core.config import (
        QDRANT_URL,
        QDRANT_API_KEY,
        COLLECTION_NAME,
        EMBEDDINGS_MODEL,
    )
from api.db.database import SessionLocal
from api.v1.models.blog import BlogPost

def get_client():

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    client.set_model(EMBEDDINGS_MODEL)
    return client

def get_all_posts():
    """Fetch all blog posts"""
    try:
        db = SessionLocal()
        posts = db.query(BlogPost).order_by(BlogPost.date.desc()).all()
        db.close()
    except Exception:
        print("Empty Database")
        posts = None

    return posts

def process_embeddings(config: dict):
    """
    Uploads or updates embeddings in Qdrant using provided config.

    Args:
        config (dict): Must contain:
            - qdrant_url
            - qdrant_api_key
            - collection_name
            - embeddings_model
            - get_content_fn (function returning list of objects with .id, .title, .content)
    """
    
    client = get_client()
    # Check if collection exists
    collections = client.get_collections()
    collection_exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections.collections
    )

    # Get content (e.g., blog posts)
    contents = config["content"]

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""],
    )

    # Prepare data for upload
    all_chunks = []
    all_metadata = []
    all_ids = []
    chunk_id = 0

    for item in contents:
        chunks = text_splitter.split_text(item.content)
        for i, chunk in enumerate(chunks):
            chunk_id += 1
            all_chunks.append(chunk)
            all_metadata.append({
                "original_id": item.id,
                "title": item.title,
                "chunk_index": i,
                "chunk_count": len(chunks),
                "page_content": chunk,
            })
            all_ids.append(chunk_id)

    if not collection_exists:
        # Create collection
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=client.get_fastembed_vector_params(on_disk=True),
            quantization_config=models.ScalarQuantization(
                scalar=models.ScalarQuantizationConfig(
                    type=models.ScalarType.INT8,
                    quantile=0.99,
                    always_ram=True,
                )
            ),
        )

        # Create payload index for LangChain compatibility
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="page_content",
            field_schema=models.TextIndexParams(
                type=models.TextIndexType.TEXT,
                tokenizer=models.TokenizerType.WORD,
                min_token_len=2,
                max_token_len=20,
                lowercase=True,
            ),
        )

        client.add(
            collection_name=COLLECTION_NAME,
            documents=all_chunks,
            metadata=all_metadata,
            ids=tqdm(all_ids),
            parallel=6,
        )
        print(f"Created collection {COLLECTION_NAME} with {len(all_chunks)} records")
    else:
        try:
            existing_ids = set(
                p.id for p in client.scroll(
                    collection_name=COLLECTION_NAME,
                    limit=100000,
                )[0]
            )
        except Exception as e:
            print(f"Error retrieving existing records: {e}")
            existing_ids = set()

        new_indices = [i for i, id_val in enumerate(all_ids) if id_val not in existing_ids]
        
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
            print(f"Added {len(new_indices)} new chunked records to {COLLECTION_NAME}")
        else:
            print("No new records to add.")

# Wrapper for existing use case
def upload_embeddings():

    blogposts = get_all_posts()
    if blogposts:
        config = {
            "content": blogposts,
        }
        process_embeddings(config)
    else:
        print("No records to add.")

async def upload_single_embeddings(new_data):
    # Run blocking get_client in a separate thread
    client = await asyncio.to_thread(get_client)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = text_splitter.split_text(new_data["content"])

    # Scroll (blocking) in thread
    scroll_result = await asyncio.to_thread(
        client.scroll,
        collection_name=COLLECTION_NAME,
        limit=100000,
    )
    existing_ids = set(p.id for p in scroll_result[0])
    last_existing_id = max(existing_ids) if existing_ids else 0

    new_ids = [i + 1 for i in range(last_existing_id, last_existing_id + len(chunks))]

    new_metadata = []
    for i, chunk in zip(new_ids, chunks):
        new_metadata.append({
            "original_id": new_data["id"],
            "title": new_data["title"],
            "chunk_index": i,
            "chunk_count": len(chunks),
            "page_content": chunk,
        })

    # Add (blocking) in thread
    await asyncio.to_thread(
        client.add,
        collection_name=COLLECTION_NAME,
        documents=chunks,
        metadata=new_metadata,
        ids=async_tqdm(new_ids),
        parallel=6,
    )

    print(f"Added {len(new_ids)} new chunked records to {COLLECTION_NAME}")


if __name__== "__main__":
    upload_embeddings()