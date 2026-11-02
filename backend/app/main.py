from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import auth, modules, circuits, simulate, ai, assess, progress
from app.content.seed import seed_db

app = FastAPI(title="QLearnAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(modules.router, prefix="/modules", tags=["modules"])
app.include_router(circuits.router, prefix="/circuits", tags=["circuits"])
app.include_router(simulate.router, prefix="/simulate", tags=["simulate"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(assess.router, prefix="/quizzes", tags=["assess"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"message": "Internal server error"})
