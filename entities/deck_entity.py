"""MySQL Deck model."""
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from entities.base_entity import mysql_base


class DeckEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela decks"""

    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    subdeck = relationship("SubDeckEntity", back_populates="deck", cascade='all, delete')
    user = relationship("UserEntity", back_populates="deck")
    review = relationship("SubDeckReviewEntity", back_populates="deck")
