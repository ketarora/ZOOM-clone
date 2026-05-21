from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MeetingCreate(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    start_time: datetime
    duration_minutes: int = Field(60, ge=5, le=1440)
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
    description: Optional[str] = None
    meeting_id: str
    passcode: Optional[str] = None
    start_time: datetime
    duration_minutes: int
    timezone: str
    waiting_room: bool
    use_passcode: bool
    is_recurring: bool
    status: str
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class JoinMeetingRequest(BaseModel):
    meeting_id: str
    name: str = Field(..., min_length=1, max_length=100)
    passcode: Optional[str] = None
    mute_audio: bool = False
    turn_off_video: bool = False
