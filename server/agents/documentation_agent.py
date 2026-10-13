import json
from rag.retriever import search_documents
from ai_client import generate_text


def retrieve_project_context(query: str, top_k: int = 8) -> str:
    documents = search_documents(query, top_k=top_k)

    if not documents:
        return ""

    context_parts = []

    for index, document in enumerate(documents, start=1):
        metadata = document.get("metadata", {})
        filename = metadata.get("filename", "unknown")

        context_parts.append(
            f"[Source {index}: {filename}]\n"
            f"{document.get('text', '')}"
        )

    return "\n\n".join(context_parts)


def generate_documentation(project_context: str) -> dict:
    if not project_context.strip():
        return {
            "user_stories": [],
            "risk_register": [],
            "action_items": []
        }

    prompt = f"""
You are a Project Documentation Generation Agent.

Generate project-management documentation using ONLY the
information provided in the PROJECT CONTEXT.

Do not invent project facts.

Return ONLY valid JSON using exactly this structure:

{{
    "user_stories": [
        {{
            "id": "US-01",
            "user_story": "...",
            "priority": "Must Have",
            "dependency": "...",
            "assignee": "..."
        }}
    ],
    "risk_register": [
        {{
            "risk_id": "R-01",
            "risk": "...",
            "impact": "High/Medium/Low",
            "likelihood": "High/Medium/Low",
            "mitigation": "...",
            "owner": "..."
        }}
    ],
    "action_items": [
        {{
            "action_id": "A-01",
            "action": "...",
            "owner": "...",
            "deadline": "...",
            "status": "Pending/In Progress/Completed"
        }}
    ]
}}

Rules:
1. Use only information present in the context.
2. Do not create fake names, dates or responsibilities.
3. If information is unavailable, use "Not specified".
4. Keep the output concise.
5. Return valid JSON only.

PROJECT CONTEXT:
{project_context}
"""

    response_text = generate_text(prompt)

    # Remove markdown JSON fences if Gemini returns them
    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "error": "The documentation agent returned invalid JSON.",
            "raw_response": response_text
        }


def generate_project_documentation() -> dict:
    queries = [
        "project user stories goals requirements deliverables",
        "project risks risk register mitigation",
        "project action items pending tasks owners deadlines"
    ]

    contexts = []

    for query in queries:
        context = retrieve_project_context(query)

        if context:
            contexts.append(context)

    combined_context = "\n\n".join(contexts)

    return generate_documentation(combined_context)