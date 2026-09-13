from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Team(Base):
    __tablename__ = 'teams'
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    slug: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    link: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    players: Mapped[list["Player"]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan",
    )