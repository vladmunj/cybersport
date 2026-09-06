from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Statistic(Base):
    __tablename__ = "statistics"
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
    team: Mapped[str] = mapped_column(
        nullable=False
    )
    rating: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        nullable=False
    )
    match: Mapped["Match"] = relationship(
        back_populates="statistics"
    )
    player: Mapped["Player"] = relationship(
        back_populates="statistics"
    )