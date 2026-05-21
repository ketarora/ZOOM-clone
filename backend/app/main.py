"""
app/main.py — FastAPI application factory
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.core.database import engine
from app.core.exceptions import not_found_handler, validation_error_handler, server_error_handler

# Import ALL models so SQLAlchemy registers them before create_all
import app.models  # noqa: F401
from app.core.database import Base

from app.routers import auth, users, meetings, recordings, chat, contacts, webinars, dashboard, websockets

settings = get_settings()
logging.basicConfig(
    level=logging.DEBUG if not settings.is_production else logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup (idempotent)."""
    logger.info("🚀 ZoomConnect API starting — env=%s", settings.ENVIRONMENT)
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables ready")
    yield
    logger.info("🛑 ZoomConnect API shutting down")


def create_app() -> FastAPI:
    app = FastAPI(
        title=f"{settings.APP_NAME} API",
        description=(
            "Enterprise Video Conferencing Platform — "
            "REST API + WebSocket signaling for ZoomConnect"
        ),
        version=settings.APP_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────
    origins = settings.cors_origins_list
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=r"https://.*\.onrender\.com" if settings.is_production else None,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception handlers ────────────────────────────────────────
    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, server_error_handler)

    # ── Health ────────────────────────────────────────────────────
    @app.get("/api/health", tags=["health"], summary="Health check")
    def health():
        from datetime import datetime, timezone
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ── Routers ───────────────────────────────────────────────────
    API_PREFIX = "/api"
    app.include_router(auth.router,       prefix=API_PREFIX)
    app.include_router(users.router,      prefix=API_PREFIX)
    app.include_router(meetings.router,   prefix=API_PREFIX)
    app.include_router(recordings.router, prefix=API_PREFIX)
    app.include_router(chat.router,       prefix=API_PREFIX)
    app.include_router(contacts.router,   prefix=API_PREFIX)
    app.include_router(webinars.router,   prefix=API_PREFIX)
    app.include_router(dashboard.router,  prefix=API_PREFIX)
    app.include_router(websockets.router)  # WS routes don't need /api prefix

    return app


app = create_app()
