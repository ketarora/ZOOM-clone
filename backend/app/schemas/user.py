from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    display_name: str
    email: str
    job_title: Optional[str] = None
    department: Optional[str] = None
    personal_meeting_id: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    avatar_url: Optional[str] = None
