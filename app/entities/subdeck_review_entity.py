"""MySQL SubDeckReviewEntity model."""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.entities.base_entity import mysql_base


class SubDeckReviewEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela subdeck_review"""

    __tablename__ = "subdeck_review"

    id = Column(Integer, primary_key=True)
    deck_review_id = Column(Integer, ForeignKey("deck_review.id"), nullable=False)
    subdeck_id = Column(Integer, ForeignKey("subdecks.id"), nullable=False)

    deck_review = relationship("DeckReviewEntity", back_populates="subdeck_review")
    card_review = relationship("CardReviewEntity", back_populates="subdeck_review")
    subdeck = relationship("SubDeckEntity", back_populates="subdeck_review")
