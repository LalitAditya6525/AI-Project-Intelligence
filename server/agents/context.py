def build_context(results: list[dict]) -> str:

    if not results:
        return ""

    context_parts = []

    for index, result in enumerate(results, start=1):

        metadata = result.get("metadata", {})

        filename = metadata.get(
            "filename",
            "unknown"
        )

        text = result.get("text", "")

        context_parts.append(
            f"[Source {index}: {filename}]\n{text}"
        )

    return "\n\n".join(context_parts)