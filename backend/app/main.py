from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.app.api.upload import router as upload_router
from backend.app.api.chat import router as chat_router
from backend.app.core.logging import setup_logger

logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("DocuMind backend started")
    yield
    logger.info("DocuMind backend stopped")


app = FastAPI(
    title="DocuMind API",
    lifespan=lifespan
)

# ✅ CORS (FIXED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/health")
def health_check():
    return {"status": "DocuMind backend running"}
