"""MySQL SubDeck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class SubDeckEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela subdecks"""

    __tablename__ = "subdecks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    creation_date = Column(DateTime)
    deck_id = Column(Integer, ForeignKey("decks.id"))

    deck = relationship("DeckEntity", back_populates="subdeck")
    card = relationship("CardEntity", back_populates="subdeck")
    review = relationship("SubDeckReviewEntity", back_populates="subdeck")
