from pydantic import BaseModel
from datetime import datetime
import uuid

from api.models.applications import ApplicationStatus


class ApplicationBaseSchema(BaseModel):
    candidate_id: uuid.UUID
    job_title: str
    status: ApplicationStatus
    applied_at: datetime


class ApplicationSchema(ApplicationBaseSchema):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ApplicationCreateSchema(BaseModel):
    job_title: str
    status: ApplicationStatus
    applied_at: datetime


class ApplicationUpdateStatusSchema(BaseModel):
    status: ApplicationStatus