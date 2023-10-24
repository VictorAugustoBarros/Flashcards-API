"""MySQL DeckReviewEntity model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from app.entities.base_entity import mysql_base


class DeckReviewEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela deck_review"""

    __tablename__ = "deck_review"

    id = Column(Integer, primary_key=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    revised = Column(Boolean(), default=False)
    revision_date = Column(DateTime(timezone=True))

    deck = relationship("DeckEntity", back_populates="deck_review")

    subdeck_review = relationship("SubDeckReviewEntity", back_populates="deck_review")
