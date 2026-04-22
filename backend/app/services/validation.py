import re
from fastapi import HTTPException


def validate_aadhaar(aadhaar: str):
    if not aadhaar.isdigit():
        raise HTTPException(status_code=400, detail="Aadhaar must contain only digits")

    if len(aadhaar) != 12:
        raise HTTPException(status_code=400, detail="Aadhaar must be exactly 12 digits")


def validate_pan(pan: str):
    pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

    if not re.match(pattern, pan):
        raise HTTPException(status_code=400, detail="Invalid PAN format")


def validate_name(name: str):
    cleaned = " ".join(name.strip().lower().split())

    if not cleaned:
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    return cleaned