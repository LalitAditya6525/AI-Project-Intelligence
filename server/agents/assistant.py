from rag.retriever import search_documents
from ai_client import generate_text


def ask_project_assistant(
    query: str,
    top_k: int = 6
) -> dict:

    if not query.strip():
        return {
            "answer": "Please enter a project-related question.",
            "sources": []
        }

    retrieved_documents = search_documents(
        query,
        top_k=top_k
    )

    if not retrieved_documents:
        return {
            "answer": (
                "I could not find this information "
                "in the uploaded documents."
            ),
            "sources": []
        }

    context_parts = []
    sources = []

    for index, document in enumerate(
        retrieved_documents,
        start=1
    ):

        metadata = document.get("metadata", {})

        filename = metadata.get(
            "filename",
            "unknown"
        )

        text = document.get(
            "text",
            ""
        )

        context_parts.append(
            f"[Source {index}: {filename}]\n{text}"
        )

        if filename not in sources:
            sources.append(filename)

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an AI Project Intelligence Assistant.

Answer the user's question using ONLY the
PROJECT CONTEXT provided below.

Important rules:

1. Do not use outside knowledge.
2. Do not invent project information.
3. Base every factual statement on the context.
4. If the information is not available, say:
   "I could not find this information in the uploaded documents."
5. When useful, mention the relevant source document.
6. For questions such as "Are we on track?",
   analyze the available project status, deadlines,
   risks and blockers from the context.
7. Keep the answer concise and useful.

PROJECT CONTEXT:

{context}

USER QUESTION:

{query}

ANSWER:
"""

    answer = generate_text(prompt)

    return {
        "answer": answer,
        "sources": sources
    }