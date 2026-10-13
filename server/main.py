from pathlib import Path
import shutil
from typing import List, Dict, Any

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Milestone 1 document ingestion and RAG
from ingestion.pdf_parser import parse_pdf
from ingestion.docx_parser import parse_docx
from ingestion.csv_parser import parse_csv
from ingestion.text_parser import parse_txt

from rag.chunks import chunk_documents
from rag.vector_store import add_documents
from rag.retriever import search_documents
from rag.generator import generate_answer

# MILESTONE 2 agents
from agents.scope_agent import extract_scope
from agents.risk_agent import detect_risks
from agents.block_agent import detect_blockers
from agents.context import build_context

# Milestone 3 agents
from agents.documentation_agent import generate_project_documentation
from agents.health_agent import calculate_project_health
from agents.assistant import ask_project_assistant


app = FastAPI(
    title="AI Project Intelligence & Risk Advisor",
    version="1.0.0",
    description="RAG-powered project intelligence backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".csv",
    ".txt"
}


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class ChatRequest(BaseModel):
    query: str
    top_k: int = 6    

# ============================================================
# MILESTONE 1
# ============================================================

def parse_document(file_path: Path, extension: str) -> Dict[str, Any]:
    """
    Helper function to parse documents based on file extension.
    """
    if extension == ".pdf":
        return parse_pdf(str(file_path))
    elif extension == ".docx":
        return parse_docx(str(file_path))
    elif extension == ".csv":
        return parse_csv(str(file_path))
    elif extension == ".txt":
        return parse_txt(str(file_path))
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )


@app.get("/")
def root():
    return {
        "message": "AI Project Intelligence & Risk Advisor API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a project document and add it to the RAG knowledge base.
    """
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {extension}. "
                "Supported types: PDF, DOCX, CSV, TXT."
            )
        )

    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text according to file type
        document = parse_document(file_path, extension)

        if not document.get("text", "").strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the document."
            )

        # Split document into chunks
        chunks = chunk_documents([document])

        # Add chunks to vector database
        added_count = add_documents(chunks)

        return {
            "message": "Document processed successfully.",
            "filename": file.filename,
            "file_type": extension,
            "characters_extracted": len(document["text"]),
            "chunks_created": len(chunks),
            "vectors_added": added_count
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )
    finally:
        file.file.close()


@app.post("/upload-multiple")
async def upload_multiple_documents(
    files: List[UploadFile] = File(
        ...,
        description="Select multiple project documents to upload"
    )
):
    """
    Upload multiple project documents at once.
    Each file is processed independently: a failure on one file
    does not abort the batch, it's just reported per-file.
    """
    if not files:
        raise HTTPException(
            status_code=400,
            detail="No files provided."
        )

    results = []

    for file in files:
        if not file.filename:
            results.append({
                "filename": None,
                "status": "failed",
                "error": "Filename is missing."
            })
            continue

        extension = Path(file.filename).suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": (
                    f"Unsupported file type: {extension}. "
                    "Supported types: PDF, DOCX, CSV, TXT."
                )
            })
            continue

        file_path = UPLOAD_DIR / file.filename

        try:
            # Save uploaded file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Extract text
            document = parse_document(file_path, extension)

            # Validate text
            if not document.get("text", "").strip():
                results.append({
                    "filename": file.filename,
                    "status": "failed",
                    "error": "No readable text found in the document."
                })
                continue

            # Chunk document & store vectors
            chunks = chunk_documents([document])
            added_count = add_documents(chunks)

            results.append({
                "filename": file.filename,
                "status": "success",
                "characters_extracted": len(document["text"]),
                "chunks_created": len(chunks),
                "vectors_added": added_count
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })
        finally:
            file.file.close()

    return {
        "message": "Batch processing completed.",
        "files": results
    }


@app.post("/query")
async def query_documents(request: QueryRequest):

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    results = search_documents(
        request.query,
        request.top_k
    )

    answer = generate_answer(
        request.query,
        results
    )

    sources = []

    for result in results:
        metadata = result.get("metadata", {})

        sources.append({
            "filename": metadata.get("filename"),
            "chunk_index": metadata.get("chunk_index"),
            "distance": result.get("distance")
        })

    return {
        "query": request.query,
        "answer": answer,
        "sources": sources
    }

# ============================================================
# MILESTONE 2
# ============================================================

@app.post("/agents/scope")
async def run_scope_agent():

    result = extract_scope()

    return {
        "agent": "scope_and_deliverable_agent",
        "result": result
    }


@app.post("/agents/risk")
async def run_risk_agent():
    result = detect_risks()

    return {
        "agent": "risk_detection_and_delivery_forecasting_agent",
        "result": result
    }


@app.post("/agents/blocker")
async def run_blocker_agent():
    result = detect_blockers()

    return {
        "agent": "blocker_and_action_item_agent",
        "result": result
    }

# ============================================================
# MILESTONE 3
# ============================================================

@app.post("/agents/documentation")
async def run_documentation_agent():
    """
    Generate project documentation from
    uploaded project information.

    Outputs:
    - User Stories
    - Risk Register
    - Action Items
    """

    try:

        result = generate_project_documentation()

        return {
            "agent": "documentation_generation_agent",
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Documentation generation failed: "
                f"{str(e)}"
            )
        )

@app.post("/agents/health")
async def run_health_agent():
    """
    Generate an overall project health score
    and dimension-wise analysis.
    """

    try:

        result = calculate_project_health()

        return {
            "agent": "project_health_scoring_agent",
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Project health calculation failed: "
                f"{str(e)}"
            )
        )

@app.post("/assistant/ask")
async def run_project_assistant(
    request: ChatRequest
):
    """
    Ask natural-language questions about
    the uploaded project documents.

    Example questions:

    - Are we on track?
    - What are our biggest risks?
    - What tasks are currently blocked?
    - What deadlines are approaching?
    """

    if not request.query.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = ask_project_assistant(
            query=request.query,
            top_k=request.top_k
        )

        return {
            "agent": "conversational_project_intelligence_assistant",
            "query": request.query,
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Assistant request failed: "
                f"{str(e)}"
            )
        )