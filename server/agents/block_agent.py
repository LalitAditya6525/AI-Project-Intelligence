import os
import json
import re
from ai_client import generate_text

from rag.retriever import search_documents



# Internal retrieval queries.
# No user query is required.
BLOCKER_QUERIES = [
    "current project blockers blocked tasks",
    "unresolved issues problems",
    "pending decisions approvals",
    "missing requirements finalized requirements",
    "action items assigned to team members",
    "meeting follow up tasks",
    "dependencies preventing progress",
    "tasks waiting for information"
]


def retrieve_blocker_context(top_k_per_query: int = 5) -> str:
    """
    Automatically retrieves project information relevant
    to blockers and action items.
    """

    all_results = []
    seen_chunks = set()

    for query in BLOCKER_QUERIES:
        results = search_documents(query, top_k_per_query)

        for result in results:
            metadata = result.get("metadata", {})

            filename = metadata.get("filename", "unknown")
            chunk_index = metadata.get("chunk_index", -1)

            chunk_id = (filename, chunk_index)

            if chunk_id in seen_chunks:
                continue

            seen_chunks.add(chunk_id)
            all_results.append(result)

    context_parts = []

    for index, result in enumerate(all_results, start=1):
        metadata = result.get("metadata", {})

        filename = metadata.get("filename", "unknown")
        chunk_index = metadata.get("chunk_index", "unknown")

        text = result.get("text", "")

        context_parts.append(
            f"""
[Source {index}]
Filename: {filename}
Chunk: {chunk_index}

{text}
"""
        )

    return "\n".join(context_parts)


def detect_blockers() -> dict:
    """
    Automatically analyzes uploaded project documents
    and identifies blockers, unresolved issues, pending
    decisions, and action items.
    """

    context = retrieve_blocker_context()

    if not context.strip():
        return {
            "blockers": [],
            "unresolved_issues": [],
            "pending_decisions": [],
            "action_items": []
        }

    prompt = f"""
You are the Blocker and Action Item Identification Agent
for an AI Project Intelligence system.

Your job is to automatically analyze the provided project
documents and identify current blockers, unresolved issues,
pending decisions, and action items.

IMPORTANT RULES:

1. Use ONLY information contained in PROJECT DOCUMENTS.
2. Do NOT use outside knowledge.
3. Do NOT invent blockers or action items.
4. Every finding must be supported by document evidence.
5. If information is unavailable, return an empty array.
6. Do not classify completed tasks as blockers.
7. Do not create an action item unless the documents indicate
   that something needs to be done.
8. Do not duplicate the same issue.

Analyze:

1. Current blockers
2. Unresolved issues
3. Pending decisions
4. Action items

For every blocker, identify:

- blocker
- description
- evidence
- affected_task
- owner
- status
- impact

For unresolved issues, identify:

- issue
- description
- evidence
- affected_area
- status

For pending decisions, identify:

- decision
- description
- evidence
- required_from
- affected_task

For action items, identify:

- action
- owner
- deadline
- status
- evidence

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT use ```json.
Do NOT provide explanations outside the JSON.

Use exactly this structure:

{{
    "blockers": [
        {{
            "blocker": "",
            "description": "",
            "evidence": "",
            "affected_task": "",
            "owner": "",
            "status": "",
            "impact": ""
        }}
    ],
    "unresolved_issues": [
        {{
            "issue": "",
            "description": "",
            "evidence": "",
            "affected_area": "",
            "status": ""
        }}
    ],
    "pending_decisions": [
        {{
            "decision": "",
            "description": "",
            "evidence": "",
            "required_from": "",
            "affected_task": ""
        }}
    ],
    "action_items": [
        {{
            "action": "",
            "owner": "",
            "deadline": "",
            "status": "",
            "evidence": ""
        }}
    ]
}}

PROJECT DOCUMENTS:

{context}
"""

    raw_response = generate_text(prompt)

    # Remove markdown code fences if Gemini accidentally returns them
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
            "error": "Blocker agent returned invalid JSON",
            "raw_response": raw_response
        }