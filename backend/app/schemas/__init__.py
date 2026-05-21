"""
app/schemas/__init__.py — re-export all schemas
"""
from app.schemas.auth import UserRegister, UserLogin, Token, TokenPayload
from app.schemas.user import UserOut, UserUpdate
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingOut, JoinMeetingRequest
from app.schemas.recording import RecordingOut
from app.schemas.chat import ChannelCreate, ChannelOut, MessageCreate, MessageOut
from app.schemas.contact import ContactCreate, ContactOut
from app.schemas.webinar import WebinarCreate, WebinarOut

__all__ = [
    "UserRegister", "UserLogin", "Token", "TokenPayload",
    "UserOut", "UserUpdate",
    "MeetingCreate", "MeetingUpdate", "MeetingOut", "JoinMeetingRequest",
    "RecordingOut",
    "ChannelCreate", "ChannelOut", "MessageCreate", "MessageOut",
    "ContactCreate", "ContactOut",
    "WebinarCreate", "WebinarOut",
]
