from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    nickname: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    fullname: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
        index=True
    )
    team: Mapped["Team"] = relationship(
        back_populates="players",
    )
    statistics: Mapped[list["Statistic"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan"
    )