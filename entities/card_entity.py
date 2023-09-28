"""MySQL User SubDeck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class CardEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela cards"""

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    question = Column(String(255))
    answer = Column(String(255))
    subdeck_id = Column(Integer, ForeignKey("subdecks.id"))
    creation_date = Column(DateTime)

    subdecks = relationship("SubDeckEntity", back_populates="cards")
