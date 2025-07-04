from api.core.db import Base
from api.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Users(BaseModel, Base):
    __tablename__ = 'users'
    
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
