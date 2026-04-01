from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.processor import process_file
from dotenv import dotenv_values

config = dotenv_values(".env")
MAX_FILE_SIZE = int(config.get("MAX_FILE_SIZE", 5000000))

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Arquivo excede o tamanho máximo permitido.")
    result = await process_file(file)
    return result