from pathlib import Path
import pandas as pd


def parse_csv(file_path: str) -> dict:
    """
    Convert CSV rows into searchable text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    if dataframe.empty:
        return {
            "text": "",
            "metadata": {
                "filename": path.name,
                "file_type": "csv",
                "source": str(path),
                "rows": 0
            }
        }

    text_parts = []

    columns = list(dataframe.columns)

    text_parts.append(
        "CSV Columns: " + ", ".join(columns)
    )

    for index, row in dataframe.iterrows():

        row_data = []

        for column in columns:

            value = row[column]

            if pd.isna(value):
                value = ""

            row_data.append(
                f"{column}: {value}"
            )

        text_parts.append(
            f"\n[Row {index + 1}]\n"
            + "\n".join(row_data)
        )

    return {
        "text": "\n".join(text_parts).strip(),
        "metadata": {
            "filename": path.name,
            "file_type": "csv",
            "source": str(path),
            "rows": len(dataframe),
            "columns": columns
        }
    }