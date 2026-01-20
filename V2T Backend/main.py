from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import database, create_tables
from app.api import routes
from app.api import auth


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth.router)
    app.include_router(routes.router)
    
    return app


app = create_application()


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    create_tables()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown."""
    await database.disconnect()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "gpt_model": settings.gpt_model if settings.enable_gpt_5_1_codex_max else "disabled",
        "gpt_5_1_codex_max_enabled": settings.enable_gpt_5_1_codex_max,
        "features": ["Authentication", "OTP Verification", "GPT-5.1-Codex-Max"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "gpt_5_1_codex_max": "enabled" if settings.enable_gpt_5_1_codex_max else "disabled",
        "authentication": "enabled"
    }
