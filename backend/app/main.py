from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analysis import router as analysis_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="X Fake Account Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router, prefix="/api", tags=["Analysis"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
