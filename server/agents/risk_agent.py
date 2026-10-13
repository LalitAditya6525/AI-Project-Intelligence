import os
import json
import re
from ai_client import generate_text

from rag.retriever import search_documents



# Internal queries used by the agent.
# The user does NOT need to provide a query.
RISK_QUERIES = [
    "project risks threats concerns problems",
    "schedule delays late overdue tasks",
    "project dependencies dependency gaps",
    "delivery deadline completion challenges",
    "testing quality issues failures",
    "missing requirements incomplete requirements",
    "blocked tasks unresolved issues",
    "API integration technical delays"
]


def retrieve_risk_context(top_k_per_query: int = 5) -> str:
    """
    Automatically retrieves project information relevant
    to risk detection.
    """

    all_results = []
    seen_chunks = set()

    for query in RISK_QUERIES:
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


def detect_risks() -> dict:
    """
    Automatically analyzes uploaded project documents
    and identifies project risks and delivery challenges.
    """

    context = retrieve_risk_context()

    if not context.strip():
        return {
            "risks": [],
            "delivery_challenges": [],
            "dependency_gaps": [],
            "schedule_risks": []
        }

    prompt = f"""
You are the Risk Detection and Delivery Forecasting Agent
for an AI Project Intelligence system.

Your job is to automatically analyze the provided project
documents and identify project risks and potential delivery
problems.

IMPORTANT RULES:

1. Use ONLY information contained in PROJECT DOCUMENTS.
2. Do NOT use outside knowledge.
3. Do NOT invent risks.
4. Every identified risk must be supported by information
   in the documents.
5. If information is not available, return an empty array.
6. Do not assume that a task is delayed unless the documents
   provide evidence of delay or schedule risk.
7. Distinguish between an existing risk and a completed task.
8. Do not duplicate the same risk.

Analyze:

1. Project risks
2. Delivery challenges
3. Dependency gaps
4. Schedule risks

For every risk, identify:

- risk
- description
- evidence
- impact
- severity
- related_task
- owner

Severity must be one of:

"Low"
"Medium"
"High"
"Critical"

For delivery challenges, identify:

- challenge
- description
- evidence
- impact

For dependency gaps, identify:

- dependency
- description
- affected_task
- evidence

For schedule risks, identify:

- task
- due_date
- current_status
- risk_description
- evidence

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT use ```json.
Do NOT provide explanations outside the JSON.

Use exactly this structure:

{{
    "risks": [
        {{
            "risk": "",
            "description": "",
            "evidence": "",
            "impact": "",
            "severity": "",
            "related_task": "",
            "owner": ""
        }}
    ],
    "delivery_challenges": [
        {{
            "challenge": "",
            "description": "",
            "evidence": "",
            "impact": ""
        }}
    ],
    "dependency_gaps": [
        {{
            "dependency": "",
            "description": "",
            "affected_task": "",
            "evidence": ""
        }}
    ],
    "schedule_risks": [
        {{
            "task": "",
            "due_date": "",
            "current_status": "",
            "risk_description": "",
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
            "error": "Risk agent returned invalid JSON",
            "raw_response": raw_response
        }