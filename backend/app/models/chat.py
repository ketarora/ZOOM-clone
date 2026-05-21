"""
app/models/chat.py — Channel, ChatMessage ORM models
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Channel(Base):
    __tablename__ = "channels"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False, unique=True)
    description = Column(String(300), nullable=True)
    is_private  = Column(Boolean, default=False)
    created_by  = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at  = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    messages = relationship("ChatMessage", back_populates="channel", cascade="all, delete-orphan")
    creator  = relationship("User", foreign_keys=[created_by])


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id           = Column(Integer, primary_key=True, index=True)
    channel_id   = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"), nullable=True)
    sender_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # DM
    content      = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")   # text | file | code | reaction
    file_url     = Column(String(300), nullable=True)
    is_edited    = Column(Boolean, default=False)
    created_at   = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    edited_at    = Column(DateTime(timezone=True), nullable=True)

    channel = relationship("Channel", back_populates="messages")
    sender  = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
