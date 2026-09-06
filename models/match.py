from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Text, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Match(Base):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    external_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True
    )
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
        index=True
    )
    date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    team1: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    team2: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    score: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    link: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    event: Mapped["Event"] = relationship(
        back_populates="matches"
    )
    maps: Mapped[list["Map"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan"
    )
    statistics: Mapped[list["Statistic"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan"
    )