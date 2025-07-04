from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid


class CandidateBaseSchema(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None


class CandidateDetailedSchema(CandidateBaseSchema):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    skills: List[str]


class CandidateUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None

    class Config:
        from_attributes = True


class CandidateSchema(CandidateDetailedSchema):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

