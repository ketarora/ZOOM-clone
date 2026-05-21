"""
app/core/database.py
SQLAlchemy engine + session factory + Base
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import get_settings


settings = get_settings()

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.ENVIRONMENT == "development",  # SQL logs in dev
)

# Enable WAL mode for SQLite (much better concurrency)
if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_wal_mode(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA journal_mode=WAL")
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency — yields a DB session and auto-closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
