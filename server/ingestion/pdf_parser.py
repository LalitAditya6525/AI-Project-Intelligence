from pathlib import Path
import pymupdf


def parse_pdf(file_path: str) -> dict:
    """
    Extract text from a PDF file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    text_parts = []

    with pymupdf.open(file_path) as pdf:

        total_pages = len(pdf)

        for page_number, page in enumerate(pdf, start=1):

            page_text = page.get_text("text")

            if page_text.strip():
                text_parts.append(
                    f"\n[Page {page_number}]\n"
                    f"{page_text}"
                )

    return {
        "text": "\n".join(text_parts).strip(),
        "metadata": {
            "filename": path.name,
            "file_type": "pdf",
            "source": str(path),
            "total_pages": total_pages
        }
    }