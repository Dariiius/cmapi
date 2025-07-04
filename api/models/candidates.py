from datetime import datetime
from typing import List, Optional
from sqlalchemy import ARRAY, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from api.core.db import Base
from api.models.base import BaseModel


class Candidates(BaseModel, Base):
    __tablename__ = 'candidates'

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    skills: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    