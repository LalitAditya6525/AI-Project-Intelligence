from pathlib import Path
from uuid import uuid4

import chromadb

from rag.embeddings import generate_embeddings


BASE_DIR = Path(__file__).resolve().parents[2]

VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"

VECTOR_DB_DIR.mkdir(
    parents=True,
    exist_ok=True
)


client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)


collection = client.get_or_create_collection(
    name="project_knowledge_base",
    metadata={
        "description": (
            "Unified project knowledge base "
            "for AI Project Intelligence"
        )
    }
)


def add_documents(
    documents: list[dict]
) -> int:
    """
    Add document chunks to ChromaDB.
    """

    if not documents:
        return 0

    texts = [
        document["text"]
        for document in documents
    ]

    embeddings = generate_embeddings(texts)

    ids = [
        str(uuid4())
        for _ in documents
    ]

    metadatas = []

    for document in documents:

        metadata = document.get(
            "metadata",
            {}
        ).copy()

        # Chroma metadata values must be simple types.
        cleaned_metadata = {}

        for key, value in metadata.items():

            if isinstance(
                value,
                (str, int, float, bool)
            ):
                cleaned_metadata[key] = value

            elif isinstance(value, list):
                cleaned_metadata[key] = ", ".join(
                    map(str, value)
                )

            else:
                cleaned_metadata[key] = str(value)

        metadatas.append(cleaned_metadata)

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(documents)


def get_collection_count() -> int:
    """
    Return number of chunks stored.
    """

    return collection.count()


def clear_collection() -> None:
    """
    Delete and recreate the knowledge base.
    """

    global collection

    client.delete_collection(
        "project_knowledge_base"
    )

    collection = client.get_or_create_collection(
        name="project_knowledge_base",
        metadata={
            "description": (
                "Unified project knowledge base "
                "for AI Project Intelligence"
            )
        }
    )