import os
from dotenv import load_dotenv
from ai_client import generate_text

load_dotenv()
    


def generate_answer(query: str, retrieved_documents: list[dict]) -> str:

    if not retrieved_documents:
        return "I could not find relevant information in the uploaded documents."

    context_parts = []

    for index, document in enumerate(
        retrieved_documents,
        start=1
    ):
        filename = document.get(
            "metadata", {}
        ).get(
            "filename",
            "unknown"
        )

        text = document.get("text", "")

        context_parts.append(
            f"[Source {index}: {filename}]\n{text}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an AI Project Intelligence Assistant.

Answer the user's question using ONLY the information
provided in the CONTEXT.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not present, say:
   "I could not find this information in the uploaded documents."
4. Give a concise answer.

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    response_text = generate_text(prompt)

    return response_text.strip()