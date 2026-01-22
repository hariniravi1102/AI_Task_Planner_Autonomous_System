# upload.py
import os
import json
from typing import List
from fastapi import UploadFile

# Base data directory
BASE_DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "data"
)

ALLOWED_EXTENSIONS = {
    ".csv",
    ".geojson",
    ".json",
    ".tif",
    ".tiff",
    ".zip"
}

# JOB DIRECTORY


def job_dir(job_id: str) -> str:
    path = os.path.join(BASE_DATA_DIR, job_id)
    os.makedirs(path, exist_ok=True)
    return path

# FILE UPLOAD


def upload_files(job_id: str, files: List[UploadFile]):
    save_dir = job_dir(job_id)
    saved = []

    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            return {
                "status": "error",
                "message": f"Unsupported file type: {file.filename}"
            }

        file_path = os.path.join(save_dir, file.filename)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        saved.append(file.filename)

    return {
        "status": "success",
        "job_id": job_id,
        "files": saved
    }

# SAVE AOI


def save_aoi(job_id: str, geojson: dict):
    path = job_dir(job_id)
    aoi_path = os.path.join(path, "aoi.geojson")

    with open(aoi_path, "w") as f:
        json.dump(geojson, f, indent=2)

    return {"status": "saved", "type": "AOI"}


# SAVE EXTERNAL TEXT


def save_external(job_id: str, text: str):
    path = job_dir(job_id)
    ext_path = os.path.join(path, "external.txt")

    with open(ext_path, "w") as f:
        f.write(text)

    return {"status": "saved", "type": "external"}
