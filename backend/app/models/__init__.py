"""
app/models/__init__.py
Import all models here so SQLAlchemy sees them when Base.metadata.create_all() is called
"""
from app.models.user import User
from app.models.meeting import Meeting, MeetingParticipant
from app.models.recording import Recording
from app.models.chat import Channel, ChatMessage
from app.models.contact import Contact, Webinar

__all__ = [
    "User",
    "Meeting",
    "MeetingParticipant",
    "Recording",
    "Channel",
    "ChatMessage",
    "Contact",
    "Webinar",
]
