from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """
    Metadata associated with an uploaded document.
    """

    filename: str
    file_type: str
    source: Optional[str] = None

    page: Optional[int] = None
    row: Optional[int] = None
    chunk_index: Optional[int] = None

    extra: Dict[str, Any] = Field(
        default_factory=dict
    )


class Document(BaseModel):
    """
    Unified internal document representation.
    """

    text: str
    metadata: DocumentMetadata