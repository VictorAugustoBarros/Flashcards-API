"""MySQL SubDeck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.entities.base_entity import mysql_base


class SubDeckEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela subdecks"""

    __tablename__ = "subdecks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)

    deck = relationship("DeckEntity", back_populates="subdeck")
    cards = relationship("CardEntity", cascade="all, delete")
    subdeck_review = relationship("SubDeckReviewEntity", back_populates="subdeck")
