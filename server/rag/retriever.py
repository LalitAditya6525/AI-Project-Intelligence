from rag.vector_store import collection
from rag.embeddings import generate_query_embedding


def search_documents(
    query: str,
    top_k: int = 5
) -> list[dict]:
    """
    Perform semantic similarity search
    against the project knowledge base.
    """

    if not query.strip():
        return []

    query_embedding = generate_query_embedding(
        query
    )

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = result.get(
        "documents",
        [[]]
    )[0]

    metadatas = result.get(
        "metadatas",
        [[]]
    )[0]

    distances = result.get(
        "distances",
        [[]]
    )[0]

    results = []

    for index, document in enumerate(documents):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        results.append({
            "text": document,
            "metadata": metadata,
            "distance": distance
        })

    return results