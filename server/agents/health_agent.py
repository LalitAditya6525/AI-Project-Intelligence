import json
from rag.retriever import search_documents
from ai_client import generate_text


def retrieve_health_context() -> str:
    queries = [
        "project scope goals requirements",
        "project milestones deadlines timeline",
        "project risks delivery challenges",
        "project blockers unresolved issues",
        "project progress status completed in progress"
    ]

    all_context = []

    for query in queries:
        documents = search_documents(query, top_k=5)

        for document in documents:
            metadata = document.get("metadata", {})
            filename = metadata.get("filename", "unknown")

            all_context.append(
                f"[Source: {filename}]\n"
                f"{document.get('text', '')}"
            )

    # Remove duplicate chunks
    unique_context = list(dict.fromkeys(all_context))

    return "\n\n".join(unique_context)


def calculate_project_health() -> dict:
    context = retrieve_health_context()

    if not context:
        return {
            "error": "No project information found."
        }

    prompt = f"""
You are a Project Health Assessment Agent.

Analyze the project using ONLY the provided project context.

Calculate scores from 0 to 100 for:

1. scope_clarity
2. timeline_health
3. risk_health
4. blocker_health

Then calculate:

overall_score

Use this formula:

overall_score =
(
scope_clarity +
timeline_health +
risk_health +
blocker_health
) / 4

Higher score means healthier project conditions.

Return ONLY valid JSON:

{{
    "overall_score": 0,
    "scope_clarity": 0,
    "timeline_health": 0,
    "risk_health": 0,
    "blocker_health": 0,
    "summary": "...",
    "dimension_analysis": {{
        "scope_clarity": "...",
        "timeline_health": "...",
        "risk_health": "...",
        "blocker_health": "..."
    }},
    "evidence": [
        "..."
    ]
}}

Rules:
- Use only information from the project context.
- Do not invent facts.
- Explain scores using evidence.
- If information is unavailable, mention it.
- Return JSON only.

PROJECT CONTEXT:
{context}
"""

    response_text = generate_text(prompt)

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "error": "Health agent returned invalid JSON.",
            "raw_response": response_text
        }