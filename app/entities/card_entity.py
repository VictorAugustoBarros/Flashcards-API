"""MySQL User SubDeck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship

from app.entities.base_entity import mysql_base


class CardEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela cards"""

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    subdeck_id = Column(Integer, ForeignKey("subdecks.id"), nullable=False)
    question = Column(String(255))
    answer = Column(String(255))
    revised = Column(Boolean(), default=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    card_review = relationship("CardReviewEntity", back_populates="card")
