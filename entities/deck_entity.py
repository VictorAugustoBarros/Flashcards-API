"""MySQL Deck model."""
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class DeckEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela decks"""

    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    creation_date = Column(DateTime)

    subdeck = relationship("SubDeckEntity", back_populates="deck")
    user = relationship("UserEntity", back_populates="deck")
    review = relationship("SubDeckReviewEntity", back_populates="deck")
