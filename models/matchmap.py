from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class MatchMap(Base):
    __tablename__ = "maps"
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False,
        index=True
    )
    map_name: Mapped[str] = mapped_column(
        String(50),
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
    match: Mapped["Match"] = relationship(
        back_populates="maps"
    )