"""
app/models/user.py — User ORM model
"""
import random
import string
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


def _generate_pmi() -> str:
    d = "".join(random.choices(string.digits, k=11))
    return f"{d[:3]} {d[3:7]} {d[7:]}"


class User(Base):
    __tablename__ = "users"

    id                  = Column(Integer, primary_key=True, index=True)
    display_name        = Column(String(100), nullable=False)
    email               = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password     = Column(String(200), nullable=False)
    job_title           = Column(String(100), nullable=True)
    department          = Column(String(100), nullable=True)
    personal_meeting_id = Column(String(20), unique=True, default=_generate_pmi)
    avatar_url          = Column(String(300), nullable=True)
    is_active           = Column(Boolean, default=True, nullable=False)
    created_at          = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at          = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    owned_meetings  = relationship("Meeting", back_populates="owner", foreign_keys="Meeting.owner_id")
    contacts        = relationship("Contact", back_populates="user",  foreign_keys="Contact.user_id")
    sent_messages   = relationship("ChatMessage", back_populates="sender", foreign_keys="ChatMessage.sender_id")
