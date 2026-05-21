from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WebinarCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    start_time: datetime
    duration_minutes: int = Field(60, ge=5, le=480)


class WebinarOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    webinar_id: str
    start_time: datetime
    duration_minutes: int
    host_id: int
    registrant_count: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
