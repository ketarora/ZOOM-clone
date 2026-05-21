from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ContactCreate(BaseModel):
    contact_user_id: Optional[int] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    group_name: Optional[str] = None


class ContactOut(BaseModel):
    id: int
    user_id: int
    contact_user_id: Optional[int] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    group_name: Optional[str] = None
    is_online: bool
    added_at: datetime

    model_config = {"from_attributes": True}
