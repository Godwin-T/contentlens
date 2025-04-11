import os.path
from qdrant_client import QdrantClient, models
from tqdm import tqdm
from api.v1.services.blog_service import get_all_posts
from api.ai_core.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    COLLECTION_NAME,
    TEXT_FIELD_NAME,
    EMBEDDINGS_MODEL,
)


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

    blogposts = get_all_posts()
    blogposts_content = [
        {"id": post.id, "title": post.title, "content": post.content}
        for post in blogposts
    ]

    # If you want to split it into documents and metadata like before:
    ids = [post["id"] for post in blogposts_content]
    documents = [post["content"] for post in blogposts_content]
    metadata = [
        {"id": post["id"], "title": post["title"]} for post in blogposts_content
    ]

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

        # Create payload index
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=TEXT_FIELD_NAME,
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
            documents=documents,
            metadata=metadata,
            ids=tqdm(ids),
            parallel=6,
        )
        print(f"Created collection {COLLECTION_NAME} with {len(documents)} records")
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
        update_indices = []

        for id_val in ids:
            if id_val in existing_ids:
                update_indices.append(id_val - 1)
            else:
                new_indices.append(id_val - 1)

        # Add new records
        if new_indices:
            new_docs = [documents[i] for i in new_indices]
            new_metadata = [metadata[i] for i in new_indices]
            new_ids = [ids[i] for i in new_indices]

            client.add(
                collection_name=COLLECTION_NAME,
                documents=new_docs,
                metadata=new_metadata,
                ids=tqdm(new_ids),
                parallel=6,
            )
            print(
                f"Added {len(new_indices)} new records to collection {COLLECTION_NAME}"
            )
        else:
            print("No changes made")

        # # Update existing records
        # if update_indices:
        #     update_docs = [documents[i] for i in update_indices]
        #     update_metadata = [metadata[i] for i in update_indices]
        #     update_ids = [ids[i] for i in update_indices]

        #     # For updates, use the add method with the `upsert` parameter set to True
        #     client.add(
        #         collection_name=COLLECTION_NAME,
        #         documents=update_docs,
        #         metadata=update_metadata,
        #         ids=tqdm(update_ids),
        #         parallel=6,
        #         upsert=True  # This will update if exists, or insert if not
        #     )
        #     print(f"Updated {len(update_indices)} existing records in collection {COLLECTION_NAME}")


if __name__ == "__main__":
    upload_or_update_embeddings()
