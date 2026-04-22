from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_file(file: UploadFile):
    filename = file.filename.lower()

    # Extension check
    if "." not in filename:
        raise HTTPException(status_code=400, detail="Invalid file name")

    ext = filename.split(".")[-1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # MIME check
    if not file.content_type.startswith(("image/", "application/pdf")):
        raise HTTPException(status_code=400, detail="Invalid MIME type")

    # Size check
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")