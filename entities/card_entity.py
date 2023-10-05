"""MySQL User SubDeck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class CardEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela cards"""

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    question = Column(String(255))
    answer = Column(String(255))
    revised = Column(Boolean(False))
    revision_date = Column(DateTime)
    creation_date = Column(DateTime)
    subdeck_id = Column(Integer, ForeignKey("subdecks.id"))
    review_difficulties_id = Column(Integer, ForeignKey("review_difficulties.id"))

    subdeck = relationship("SubDeckEntity", back_populates="card")
    review_difficulties = relationship(
        "ReviewDifficultiesEntity", back_populates="card"
    )
