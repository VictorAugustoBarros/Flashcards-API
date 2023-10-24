"""MySQL CardReviewEntity model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.entities.base_entity import mysql_base


class CardReviewEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela card_review"""

    __tablename__ = "card_review"

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    subdeck_review_id = Column(Integer, ForeignKey("subdeck_review.id"), nullable=False)
    review_difficulties_id = Column(
        Integer, ForeignKey("review_difficulties.id"), nullable=False
    )
    revision_date = Column(DateTime(timezone=True))

    subdeck_review = relationship("SubDeckReviewEntity", back_populates="card_review")
    review_difficulties = relationship(
        "ReviewDifficultiesEntity", back_populates="card_review"
    )
    card = relationship("CardEntity", back_populates="card_review")
