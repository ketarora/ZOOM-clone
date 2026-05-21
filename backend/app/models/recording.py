"""
app/models/recording.py — Cloud & local recording model
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Recording(Base):
    __tablename__ = "recordings"

    id               = Column(Integer, primary_key=True, index=True)
    meeting_id       = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    title            = Column(String(200), nullable=False)
    file_url         = Column(String(300), nullable=True)
    thumbnail_url    = Column(String(300), nullable=True)
    duration_seconds = Column(Integer, default=0)
    file_size_mb     = Column(Integer, default=0)
    status           = Column(String(20), default="processing")  # processing | ready
    storage_type     = Column(String(10), default="cloud")       # cloud | local
    host_id          = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recorded_at      = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    meeting = relationship("Meeting", back_populates="recordings")
    host    = relationship("User", foreign_keys=[host_id])
