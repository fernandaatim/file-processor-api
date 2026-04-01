from fastapi import FastAPI
from app.routes.upload import router as upload_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="File Processor API")
app.include_router(upload_router)