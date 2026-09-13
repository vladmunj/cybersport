from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Map(Base):
    __tablename__ = 'maps'
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    matches: Mapped[list["MatchMap"]] = relationship(
        back_populates="map",
        cascade="all, delete-orphan"
    )