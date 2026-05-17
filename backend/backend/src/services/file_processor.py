import os
import uuid
import pathlib
import fastapi
from fastapi import UploadFile
from typing import Tuple

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB default

async def validate_file(file: UploadFile, max_size: int = MAX_FILE_SIZE_BYTES) -> Tuple[str, int]:
    """
    Validates file extension and size.
    Returns (file_extension, file_size).
    """
    filename = file.filename or ""
    extension = pathlib.Path(filename).suffix.lower()
    
    if extension not in ALLOWED_EXTENSIONS:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {extension}. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file to check size
    content = await file.read()
    file_size = len(content)
    
    if file_size > max_size:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {max_size // (1024*1024)}MB limit"
        )
    
    # Seek back to start for subsequent reads if needed, 
    # but we already have the content. We'll return it or write it directly.
    # For now, let's just return the size and extension.
    # Resetting the cursor just in case.
    await file.seek(0)
    
    return extension, file_size

import tempfile

async def save_upload_file(file: UploadFile, subfolder: str) -> Tuple[str, str]:
    """
    Saves an uploaded file temporarily to the specified subfolder.
    Returns (stored_filename, absolute_path).
    """
    # Use temporary directory instead of permanent uploads folder
    upload_dir = pathlib.Path(tempfile.gettempdir()) / "samvaad_sathi_uploads" / subfolder
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    extension = pathlib.Path(file.filename or "").suffix.lower()
    stored_filename = f"{uuid.uuid4()}{extension}"
    file_path = upload_dir / stored_filename
    
    # Write file content
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
        
    return stored_filename, str(file_path).replace("\\", "/")
