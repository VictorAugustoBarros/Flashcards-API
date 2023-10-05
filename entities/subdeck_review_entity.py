"""MySQL SubDeckReviewEntity model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class SubDeckReviewEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela subdeck_review"""

    __tablename__ = "subdeck_review"

    id = Column(Integer, primary_key=True)
    deck_id = Column(Integer, ForeignKey("decks.id"))
    subdeck_id = Column(Integer, ForeignKey("subdecks.id"))
    creation_date = Column(DateTime)

    deck = relationship("DeckEntity", back_populates="review")
    subdeck = relationship("SubDeckEntity", back_populates="review")
