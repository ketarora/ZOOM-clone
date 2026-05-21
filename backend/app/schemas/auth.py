from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    display_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)

    @field_validator("display_name")
    @classmethod
    def name_no_spaces_only(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Display name cannot be blank")
        return v.strip()


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
