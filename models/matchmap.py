from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.maps import Map


class MatchMap(Base):
    __tablename__ = "match_maps"
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False,
        index=True
    )
    map_id: Mapped[int] = mapped_column(
        ForeignKey("maps.id"),
        nullable=False,
        index=True
    )
    score: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    match: Mapped["Match"] = relationship(
        back_populates="maps"
    )
    map: Mapped["Map"] = relationship(
        back_populates="matches"
    )