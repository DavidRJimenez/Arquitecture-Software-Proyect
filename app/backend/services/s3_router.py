from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from .s3_service import upload_file, list_files, delete_file

router = APIRouter(prefix="/s3", tags=["s3"])

@router.post("/upload", response_model=str)
async def upload_endpoint(file: UploadFile = File(...)):
    try:
        url = upload_file(file.file, file.filename)
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=List[str])
async def list_endpoint():
    try:
        return list_files()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{filename}", response_model=bool)
async def delete_endpoint(filename: str):
    try:
        return delete_file(filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))