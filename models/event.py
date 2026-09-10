from datetime import date, datetime
from sqlalchemy import Date, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    slug: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    link: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    matches: Mapped[list["Match"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )