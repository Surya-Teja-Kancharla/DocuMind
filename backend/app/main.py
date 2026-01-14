from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.app.api.upload import router as upload_router
from backend.app.api.chat import router as chat_router
from backend.app.core.logging import setup_logger

logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("DocuMind backend started")
    yield
    # Shutdown logic
    logger.info("DocuMind backend stopped")


app = FastAPI(
    title="DocuMind API",
    lifespan=lifespan
)

# Routers
app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/health")
def health_check():
    return {"status": "DocuMind backend running"}
