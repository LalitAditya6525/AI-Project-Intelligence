from pathlib import Path


def parse_txt(file_path: str) -> dict:
    """
    Read a plain text file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Text file not found: {file_path}"
        )

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            text = file.read()

    except UnicodeDecodeError:

        with open(
            file_path,
            "r",
            encoding="latin-1"
        ) as file:
            text = file.read()

    return {
        "text": text.strip(),
        "metadata": {
            "filename": path.name,
            "file_type": "txt",
            "source": str(path)
        }
    }