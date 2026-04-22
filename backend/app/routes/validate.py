from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.utils.security import validate_file
from app.utils.file_handler import save_file

from app.services.validation import (
    validate_aadhaar,
    validate_pan,
    validate_name
)

from app.services.ocr_service import extract_text

from app.services.parser import (
    extract_aadhaar,
    extract_pan,
    extract_name
)

from difflib import SequenceMatcher


router = APIRouter()


# -----------------------------
# SIMILARITY FUNCTION
# -----------------------------
def similarity(a, b):
    if not a or not b:
        return 0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


@router.post("/validate")
async def validate_identity(
    name: str = Form(...),
    aadhaar_number: str = Form(...),
    pan_number: str = Form(...),
    aadhaar_file: UploadFile = File(...),
    pan_file: UploadFile = File(...)
):
    # -----------------------------
    # NORMALIZE INPUT
    # -----------------------------
    aadhaar_number = aadhaar_number.replace(" ", "")
    pan_number = pan_number.upper()

    # -----------------------------
    # VALIDATE INPUT FORMAT
    # -----------------------------
    cleaned_name = validate_name(name)
    validate_aadhaar(aadhaar_number)
    validate_pan(pan_number)

    # -----------------------------
    # VALIDATE FILES
    # -----------------------------
    validate_file(aadhaar_file)
    validate_file(pan_file)

    # -----------------------------
    # SAVE FILES
    # -----------------------------
    try:
        aadhaar_path = await save_file(aadhaar_file, "aadhaar")
        pan_path = await save_file(pan_file, "pan")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File saving failed: {str(e)}")

    # -----------------------------
    # OCR
    # -----------------------------
    aadhaar_text = extract_text(aadhaar_path)
    pan_text = extract_text(pan_path)

    # -----------------------------
    # PARSING
    # -----------------------------
    aadhaar_extracted = extract_aadhaar(aadhaar_text)
    pan_extracted = extract_pan(pan_text)
    name_extracted = extract_name(aadhaar_text)

    # -----------------------------
    # MATCHING
    # -----------------------------
    aadhaar_match = aadhaar_number == aadhaar_extracted
    pan_match = pan_number == pan_extracted

    name_similarity_score = similarity(cleaned_name, name_extracted)
    name_match = name_similarity_score > 0.7

    # -----------------------------
    # FINAL DECISION ENGINE
    # -----------------------------
    errors = []
    warnings = []
    success_checks = []

    # Aadhaar checks
    if not aadhaar_extracted:
        errors.append("Aadhaar number not found in document")
    elif not aadhaar_match:
        errors.append("Aadhaar number does not match")
    else:
        success_checks.append("Aadhaar verified")

    # PAN checks
    if not pan_extracted:
        errors.append("PAN number not found in document")
    elif not pan_match:
        errors.append("PAN number does not match")
    else:
        success_checks.append("PAN verified")

    # Name checks
    if not name_extracted:
        warnings.append("Name not clearly detected")
    elif not name_match:
        errors.append("Name does not match document")
    else:
        success_checks.append("Name verified")

    # -----------------------------
    # FINAL STATUS
    # -----------------------------
    if errors:
        status = "failed"
        message = "Validation failed"
    elif warnings:
        status = "partial"
        message = "Validation partially successful"
    else:
        status = "success"
        message = "All validations passed"

    # -----------------------------
    # RESPONSE
    # -----------------------------
    return {
        "status": status,
        "message": message,
        "errors": errors,
        "warnings": warnings,
        "success": success_checks,
        "data": {
            "input": {
                "name": cleaned_name,
                "aadhaar_number": aadhaar_number,
                "pan_number": pan_number
            },
            "extracted": {
                "aadhaar_number": aadhaar_extracted,
                "pan_number": pan_extracted,
                "name": name_extracted
            },
            "confidence": {
                "name_similarity": round(name_similarity_score, 2)
            }
        }
    }