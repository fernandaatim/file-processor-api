from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.security.api_key import APIKeyHeader
from app.services.processor import process_file
from dotenv import dotenv_values

config = dotenv_values(".env")
MAX_FILE_SIZE = int(config.get("MAX_FILE_SIZE", 5000000))
API_KEY = config.get("API_KEY",)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), api_key: str = api_key_header):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Chave de API inválida.")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Arquivo excede o tamanho máximo permitido.")
    
    result = await process_file(file, contents)
    return result