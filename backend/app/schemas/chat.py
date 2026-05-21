from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChannelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    description: Optional[str] = Field(None, max_length=300)
    is_private: bool = False


class ChannelOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_private: bool
    created_by: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)
    message_type: str = "text"
    file_url: Optional[str] = None


class MessageOut(BaseModel):
    id: int
    channel_id: Optional[int] = None
    sender_id: int
    recipient_id: Optional[int] = None
    content: str
    message_type: str
    is_edited: bool
    created_at: datetime

    model_config = {"from_attributes": True}
