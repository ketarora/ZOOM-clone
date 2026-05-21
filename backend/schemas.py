"""
ZoomConnect Backend — FastAPI
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ─── Auth ───────────────────────────────────────────
class UserRegister(BaseModel):
    display_name: str
    email: EmailStr
    password: str
    job_title: Optional[str] = None
    department: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ─── User ───────────────────────────────────────────
class UserOut(BaseModel):
    id: int
    display_name: str
    email: str
    job_title: Optional[str]
    department: Optional[str]
    personal_meeting_id: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None


# ─── Meeting ─────────────────────────────────────────
class MeetingCreate(BaseModel):
    topic: str
    description: Optional[str] = None
    start_time: datetime
    duration_minutes: int = 60
    timezone: str = "UTC"
    waiting_room: bool = True
    use_passcode: bool = True
    is_recurring: bool = False


class MeetingUpdate(BaseModel):
    topic: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    waiting_room: Optional[bool] = None
    use_passcode: Optional[bool] = None


class MeetingOut(BaseModel):
    id: int
    topic: str
    description: Optional[str]
    meeting_id: str
    passcode: Optional[str]
    start_time: datetime
    duration_minutes: int
    timezone: str
    waiting_room: bool
    use_passcode: bool
    is_recurring: bool
    status: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class JoinMeetingRequest(BaseModel):
    meeting_id: str
    name: str
    passcode: Optional[str] = None
    mute_audio: bool = False
    turn_off_video: bool = False


# ─── Recording ───────────────────────────────────────
class RecordingOut(BaseModel):
    id: int
    title: str
    file_url: Optional[str]
    thumbnail_url: Optional[str]
    duration_seconds: int
    file_size_mb: int
    status: str
    host_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


# ─── Chat ────────────────────────────────────────────
class ChannelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_private: bool = False


class ChannelOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_private: bool
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str
    channel_id: Optional[int] = None
    recipient_id: Optional[int] = None
    message_type: str = "text"


class MessageOut(BaseModel):
    id: int
    channel_id: Optional[int]
    sender_id: int
    recipient_id: Optional[int]
    content: str
    message_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Contact ─────────────────────────────────────────
class ContactCreate(BaseModel):
    contact_user_id: Optional[int] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    group_name: Optional[str] = None


class ContactOut(BaseModel):
    id: int
    user_id: int
    contact_user_id: Optional[int]
    contact_name: Optional[str]
    contact_email: Optional[str]
    phone: Optional[str]
    group_name: Optional[str]
    is_online: bool
    added_at: datetime

    class Config:
        from_attributes = True


# ─── Webinar ─────────────────────────────────────────
class WebinarCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    duration_minutes: int = 60


class WebinarOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    webinar_id: str
    start_time: datetime
    duration_minutes: int
    host_id: int
    registrant_count: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
