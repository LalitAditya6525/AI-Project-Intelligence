import os
import json
import re

from ai_client import generate_text

from rag.retriever import search_documents



# Different searches help the agent collect all
# information required for project scope extraction.
SCOPE_QUERIES = [
    "project goals objectives purpose",
    "project deliverables modules features",
    "project milestones phases development stages",
    "project deadlines important dates timeline",
    "project team members responsibilities assigned tasks"
]


def retrieve_scope_context(top_k_per_query: int = 5) -> str:

    all_results = []
    seen_chunks = set()

    for query in SCOPE_QUERIES:

        results = search_documents(
            query,
            top_k_per_query
        )

        for result in results:

            metadata = result.get("metadata", {})

            filename = metadata.get(
                "filename",
                "unknown"
            )

            chunk_index = metadata.get(
                "chunk_index",
                -1
            )

            # Prevent duplicate chunks
            chunk_id = (
                filename,
                chunk_index
            )

            if chunk_id in seen_chunks:
                continue

            seen_chunks.add(chunk_id)

            all_results.append(result)

    context_parts = []

    for index, result in enumerate(
        all_results,
        start=1
    ):

        metadata = result.get(
            "metadata",
            {}
        )

        filename = metadata.get(
            "filename",
            "unknown"
        )

        chunk_index = metadata.get(
            "chunk_index",
            "unknown"
        )

        text = result.get(
            "text",
            ""
        )

        context_parts.append(
            f"""
[Source {index}]
Filename: {filename}
Chunk: {chunk_index}

{text}
"""
        )

    return "\n".join(context_parts)


def extract_scope() -> dict:

    context = retrieve_scope_context()

    if not context.strip():

        return {
            "project_goal": "",
            "major_deliverables": [],
            "milestones": [],
            "deadlines": [],
            "team_responsibilities": [],
            "important_project_dates": []
        }

    prompt = f"""
You are the Scope and Deliverable Extraction Agent
for an AI Project Intelligence system.

Your job is to automatically analyze the provided
project documents and extract project scope information.

IMPORTANT:

Use ONLY the information contained in the provided
PROJECT DOCUMENTS.

Do not use outside knowledge.

Do not invent information.

If a particular piece of information cannot be found,
return an empty array [] or an empty string "".

Extract the following:

1. Project goal
2. Major deliverables
3. Milestones
4. Deadlines
5. Team responsibilities
6. Important project dates

For team responsibilities, identify:
- person's name
- role
- responsibility

For deadlines, identify:
- description
- date

For milestones, identify:
- milestone name
- description
- date if available

For important dates, identify:
- description
- date

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT use ```json.
Do NOT provide explanations.

Use exactly this structure:

{{
    "project_goal": "",
    "major_deliverables": [],
    "milestones": [],
    "deadlines": [],
    "team_responsibilities": [],
    "important_project_dates": []
}}

PROJECT DOCUMENTS:

{context}
"""

    raw_response = generate_text(prompt)

    # Remove accidental markdown code fences
    raw_response = re.sub(
        r"^```json\s*",
        "",
        raw_response,
        flags=re.IGNORECASE
    )

    raw_response = re.sub(
        r"\s*```$",
        "",
        raw_response
    )

    try:

        return json.loads(raw_response)

    except json.JSONDecodeError:

        return {
            "error": "Scope agent returned invalid JSON",
            "raw_response": raw_response
        }