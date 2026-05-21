"""
app/models/contact.py — Contact directory model
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    contact_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    contact_name    = Column(String(100), nullable=True)
    contact_email   = Column(String(150), nullable=True)
    phone           = Column(String(30), nullable=True)
    group_name      = Column(String(50), nullable=True)
    is_online       = Column(Boolean, default=False)
    added_at        = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user         = relationship("User", back_populates="contacts", foreign_keys=[user_id])
    contact_user = relationship("User", foreign_keys=[contact_user_id])


class Webinar(Base):
    __tablename__ = "webinars"

    id                = Column(Integer, primary_key=True, index=True)
    title             = Column(String(200), nullable=False)
    description       = Column(String(500), nullable=True)
    webinar_id        = Column(String(20), unique=True, index=True)
    start_time        = Column(DateTime(timezone=True), nullable=False)
    duration_minutes  = Column(Integer, default=60)
    host_id           = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    registrant_count  = Column(Integer, default=0)
    status            = Column(String(20), default="scheduled")
    created_at        = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    host = relationship("User", foreign_keys=[host_id])
