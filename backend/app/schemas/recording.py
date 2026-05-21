from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RecordingOut(BaseModel):
    id: int
    title: str
    file_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_seconds: int
    file_size_mb: int
    status: str
    storage_type: str
    host_id: int
    recorded_at: datetime

    model_config = {"from_attributes": True}
