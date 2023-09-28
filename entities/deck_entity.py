"""MySQL Deck model."""
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class DeckEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela decks"""

    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    creation_date = Column(DateTime)

    subdecks = relationship("SubDeckEntity", back_populates="deck")
    deck_user = relationship("UserDeckEntity", back_populates="deck")
