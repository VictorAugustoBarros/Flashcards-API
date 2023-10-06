"""MySQL SubDeckReviewEntity model."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class ReviewDifficultiesEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela review_difficulties"""

    __tablename__ = "review_difficulties"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    minutes = Column(Integer)

    card = relationship("CardEntity", back_populates="review_difficulties")
