from fastapi import HTTPException
from fastapi import UploadFile
from typing import List, Optional

def validate_guest_id(guest_id: str):
    """Ensure the guest_id is provided and not empty."""
    if not guest_id or not guest_id.strip():
        raise HTTPException(400, "guest_id is required")

def validate_files(files: Optional[List[UploadFile]]):
    """Ensure at least one file is uploaded."""
    if not files or len(files) == 0:
        raise HTTPException(400, "No files uploaded")

def validate_question(question: str):
    """Ensure the question is provided and not empty."""
    if not question or not question.strip():
        raise HTTPException(400, "Question cannot be empty")