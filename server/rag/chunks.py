from typing import List, Dict

from langchain_text_splitters import RecursiveCharacterTextSplitter


# Initial configuration for Round 1
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def chunk_documents(
    documents: List[Dict]
) -> List[Dict]:
    """
    Split extracted documents into smaller chunks.

    Each chunk preserves the original document metadata.
    """

    all_chunks = []

    for document in documents:

        text = document.get("text", "")
        metadata = document.get("metadata", {})

        if not text.strip():
            continue

        chunks = text_splitter.split_text(text)

        for chunk_index, chunk in enumerate(chunks):

            chunk_metadata = metadata.copy()

            chunk_metadata.update({
                "chunk_index": chunk_index,
                "chunk_size": len(chunk)
            })

            all_chunks.append({
                "text": chunk,
                "metadata": chunk_metadata
            })

    return all_chunks