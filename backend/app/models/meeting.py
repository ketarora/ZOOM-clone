"""
app/models/meeting.py — Meeting, MeetingParticipant ORM models
"""
import random
import string
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


def _gen_meeting_id() -> str:
    d = "".join(random.choices(string.digits, k=11))
    return f"{d[:3]} {d[3:7]} {d[7:]}"


def _gen_passcode() -> str:
    return "".join(random.choices(string.digits, k=6))


class Meeting(Base):
    __tablename__ = "meetings"

    id               = Column(Integer, primary_key=True, index=True)
    topic            = Column(String(200), nullable=False)
    description      = Column(Text, nullable=True)
    meeting_id       = Column(String(20), unique=True, index=True, default=_gen_meeting_id)
    passcode         = Column(String(20), default=_gen_passcode)
    start_time       = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=60, nullable=False)
    timezone         = Column(String(50), default="UTC")
    waiting_room     = Column(Boolean, default=True)
    use_passcode     = Column(Boolean, default=True)
    is_recurring     = Column(Boolean, default=False)
    status           = Column(String(20), default="scheduled")  # scheduled | started | ended
    recording_url    = Column(String(300), nullable=True)
    owner_id         = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at       = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at       = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))

    owner        = relationship("User", back_populates="owned_meetings", foreign_keys=[owner_id])
    participants = relationship("MeetingParticipant", back_populates="meeting", cascade="all, delete-orphan")
    recordings   = relationship("Recording", back_populates="meeting", cascade="all, delete-orphan")


class MeetingParticipant(Base):
    __tablename__ = "meeting_participants"

    id         = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    guest_name = Column(String(100), nullable=True)
    joined_at  = Column(DateTime(timezone=True), nullable=True)
    left_at    = Column(DateTime(timezone=True), nullable=True)

    meeting = relationship("Meeting", back_populates="participants")
