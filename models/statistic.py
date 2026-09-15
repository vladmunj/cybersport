from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, func, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from datetime import datetime

class Statistic(Base):
    __tablename__ = "statistics"
    __table_args__ = (
        UniqueConstraint(
            "match_id",
            "player_id",
            "team_id",
            name="uq_statistics_match_player_team",
        ),
    )
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False,
        index=True
    )
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
        index=True
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
        index=True
    )
    rating: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    match: Mapped["Match"] = relationship(
        back_populates="statistics"
    )
    player: Mapped["Player"] = relationship(
        back_populates="statistics"
    )