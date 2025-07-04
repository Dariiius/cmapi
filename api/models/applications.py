import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from api.core.db import Base
from api.models.base import BaseModel


class ApplicationStatus(str, Enum):
    APPLIED = 'applied'
    INTERVIEWING = 'interviewing'
    REJECTED = 'rejected'
    HIRED = 'hired'


class Applications(BaseModel, Base):
    __tablename__ = 'applications'

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('candidates.id'), nullable=False
    )
    job_title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[ApplicationStatus] = mapped_column(SQLEnum(ApplicationStatus), nullable=False)
    applied_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
