import os
import uuid

UPLOAD_DIR = "backend/uploads"


async def save_file(file, folder: str):
    ext = file.filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"

    folder_path = os.path.join(UPLOAD_DIR, folder)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, unique_name)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return file_path