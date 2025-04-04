---
tags: [scratchpad]
info: aberto.
date: 2025-04-04
type: post
layout: post
published: true
slug: random-python-code-to-examine
title: 'random python code to examine'
---
import io
import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional, List
from urllib.parse import urlparse # <--- Add this import

import openai
import requests # <--- Add this import
from fastapi import FastAPI, UploadFile, File, HTTPException, status, Depends, BackgroundTasks, Form, Query
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from core.markitdown import MarkItDown
from core.base import DocumentConverterResult
from core.model_manager import ModelConfigurator
from repository.db import get_db, Job

# Security validation
security = HTTPBearer()

# Get API key from environment variables
API_KEY = os.getenv("MARKIT_API_KEY", "secret-key")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
MINER_RUNNING_DEVICE = os.getenv("MINER_RUNNING_DEVICE", "cpu")
port = int(os.getenv("PORT", 20926))


# Dependency: Verify API Key
async def verify_api_key(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.scheme != "Bearer" or credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return credentials


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan management for service startup and shutdown"""
    try:
        # Initialize models
        configurator = ModelConfigurator(
            device=os.getenv("MINERU_DEVICE", MINER_RUNNING_DEVICE),
            use_modelscope=os.getenv("MINERU_USE_MODELSCOPE", "true").lower() in ("true", "1")
        )
        configurator.setup_environment()
        print("Model initialization complete")
    except Exception as e:
        print(f"Model initialization failed: {str(e)}")
        raise

    yield  # During application runtime

    # Cleanup logic (optional)
    print("Service shutting down, cleaning up resources...")


# FastAPI application
app = FastAPI(lifespan=lifespan)
if not os.path.exists("output/images"):
    os.makedirs("output/images", exist_ok=True) # Use makedirs and exist_ok=True
app.mount("/images", StaticFiles(directory="output/images"), name="images")


# Data models
class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    filename: str
    params: dict
    error: Optional[str]


class JobResultResponse(BaseModel):
    job_id: str
    download_url: str
    format: str

# --- Add this Pydantic model for the URL request ---
class UrlUploadRequest(BaseModel):
    url: str
    mode: str = "simple"
# --- End of addition ---

oai_client = None
if os.getenv("MARKIFY_LLM_API_KEY", None) and os.getenv("MARKIFY_LLM_API_BASE", None):
    oai_client = openai.OpenAI(
        api_key=os.getenv("MARKIFY_LLM_API_KEY", None),
        base_url=os.getenv("MARKIFY_LLM_API_BASE", None)
    )


def process_file(db: Session, job_id: str, file_content: bytes, filename: str, mode: str = "simple"):
    """Background task to process various files"""
    job = db.query(Job).filter(Job.id == job_id).first() # Get job first
    if not job:
        print(f"Error: Job {job_id} not found in process_file") # Add logging
        # Optionally, handle this case, e.g., log and exit,
        # but avoid committing if job doesn't exist.
        return

    try:
        # Update task status to processing
        job.status = "processing"
        db.commit()
        db.refresh(job) # Refresh to get updated state

        # Create processor
        markitdown = MarkItDown(mode=mode,
                                llm_client=oai_client,
                                llm_model=os.getenv("MARKIFY_LLM_MODEL", None)
                                )

        # Process based on input type
        if filename.endswith('.md'):
            result = DocumentConverterResult(text_content=file_content.decode('utf-8'))
        else:
            # Convert bytes content to file stream
            file_stream = io.BytesIO(file_content)
            # Pass the base_url for image path replacement if needed by converters
            result = markitdown.convert_stream(file_stream, base_url=f"http://localhost:{port}")

        # Save result to file
        output_file = OUTPUT_DIR / f"{job_id}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.text_content)

        # Update task status to completed
        job.status = "completed"
        job.result_file = str(output_file)
        db.commit()

    except Exception as e:
        # Update task status to failed ONLY IF job exists
        print(f"Error processing job {job_id}: {type(e).__name__}: {str(e)}") # Add logging
        job.status = "failed"
        job.error = f"{type(e).__name__}: {str(e)}"
        db.commit()


@app.post("/api/jobs", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        mode: str = Form("simple"),
        db: Session = Depends(get_db)
):
    """Upload file and start conversion task"""
    # Generate task ID
    job_id = str(uuid.uuid4())

    try:
        # Read file content
        content = await file.read()

        # Create task record
        job = Job(
            id=job_id,
            filename=file.filename,
            params={"mode": mode},
            status="pending"
        )
        db.add(job)
        db.commit()
        db.refresh(job) # Get the committed state

        # Start background task
        background_tasks.add_task(
            process_file,
            db=db,
            job_id=job_id,
            file_content=content,
            filename=file.filename,
            mode=mode
        )

        return {"job_id": job_id}

    except Exception as e:
        # If job creation failed, maybe rollback or log specifically
        print(f"Error during file upload for job {job_id}: {e}") # Add logging
        # Consider removing the potentially failed job entry if appropriate
        # db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload failed: {str(e)}"
        )

# --- Add this new endpoint function ---
@app.post("/api/jobs/url", status_code=status.HTTP_202_ACCEPTED)
async def upload_url(
        request_data: UrlUploadRequest, # Use the Pydantic model
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """Submit URL and start conversion task"""
    job_id = str(uuid.uuid4())
    url = request_data.url
    mode = request_data.mode

    try:
        # Download content from URL
        print(f"Attempting to download URL: {url}") # Add logging
        response = requests.get(url, stream=True, timeout=30) # Add timeout
        response.raise_for_status()  # Raise exception for bad status codes (4xx or 5xx)

        # Read content
        content = response.content # Read all content into memory for now
        print(f"Successfully downloaded {len(content)} bytes from {url}") # Add logging

        # Try to get filename from Content-Disposition header
        filename = None
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filenames = re.findall('filename="?([^"]+)"?', content_disposition)
            if filenames:
                filename = filenames[0]

        # Fallback to getting filename from URL path
        if not filename:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename: # Handle case where URL path ends in /
                 filename = f"downloaded_{job_id}" # Default filename

        print(f"Determined filename: {filename}") # Add logging

        # Create task record
        job = Job(
            id=job_id,
            filename=filename, # Use derived filename
            params={"mode": mode, "source_url": url}, # Store URL in params
            status="pending"
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # Start background task
        background_tasks.add_task(
            process_file,
            db=db,
            job_id=job_id,
            file_content=content, # Pass downloaded content
            filename=filename,    # Pass derived filename
            mode=mode
        )

        return {"job_id": job_id}

    except requests.exceptions.RequestException as e:
        print(f"Failed to download URL {url}: {e}") # Add logging
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to download URL: {str(e)}"
        )
    except Exception as e:
        # Catch other potential errors during job creation/dispatch
        print(f"Error processing URL upload for job {job_id}: {e}") # Add logging
        # db.rollback() # Consider rollback if job creation failed mid-way
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"URL processing failed: {str(e)}"
        )
# --- End of new endpoint function ---


@app.get("/api/jobs", response_model=List[JobStatusResponse])
async def list_jobs(
        db: Session = Depends(get_db),
        page: int = Query(0, ge=0, description="Page number"),
        limit: int = Query(10, gt=0, le=100, description="Items per page, default 10, max 100")):
    """Query task status list"""
    jobs = db.query(Job).order_by(Job.created_at.desc()).limit(limit).offset(page * limit).all()

    # --- Modify this part to return 200 with empty list instead of 404 ---
    # if not jobs:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="No jobs found" # Changed detail message
    #     )
    # --- End of modification ---

    response_list = []
    for job in jobs:
        response_list.append(JobStatusResponse(
            job_id=job.id,
            status=job.status,
            filename=job.filename,
            params=job.params,
            error=job.error
            # Consider adding created_at if needed by frontend:
            # created_at=job.created_at.isoformat() if job.created_at else None
        ))
    return response_list # Returns empty list [] if no jobs found, with 200 OK status


@app.get("/api/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
        job_id: str,
        db: Session = Depends(get_db)
):
    """Query task status"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        filename=job.filename,
        params=job.params,
        error=job.error
        # Consider adding created_at if needed by frontend:
        # created_at=job.created_at.isoformat() if job.created_at else None
    )


@app.get("/api/jobs/{job_id}/result")
async def download_result(
        job_id: str,
        db: Session = Depends(get_db)
):
    """Download task result file"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    if job.status != "completed":
        # Use 400 Bad Request or 404 Not Found might be better than 425 Too Early
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job status is '{job.status}', not 'completed'"
        )

    result_file = job.result_file
    if not result_file or not os.path.exists(result_file):
        # If job is completed but file missing, it's an internal server error
        print(f"Error: Result file not found for completed job {job_id} at path {result_file}") # Add logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, # Changed status code
            detail="Result file not found on server"
        )

    # Return file content
    # Use original filename for download if available, otherwise fallback
    download_filename = f"{job.filename}.md" if job.filename else f"{job_id}.md"
    return FileResponse(
        result_file,
        filename=download_filename,
        media_type="text/markdown"
    )


if __name__ == "__main__":
    import uvicorn
    # Use 127.0.0.1 for local development consistency
    uvicorn.run(app, host="127.0.0.1", port=port)

