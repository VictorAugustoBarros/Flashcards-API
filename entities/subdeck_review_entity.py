"""MySQL SubDeckReviewEntity model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class SubDeckReviewEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela subdeck_review"""

    __tablename__ = "subdeck_review"

    id = Column(Integer, primary_key=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    subdeck_id = Column(Integer, ForeignKey("subdecks.id"), nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    deck = relationship("DeckEntity", back_populates="review")
    subdeck = relationship("SubDeckEntity", back_populates="review")
