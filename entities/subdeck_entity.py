"""MySQL SubDeck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class SubDeckEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela subdecks"""

    __tablename__ = "subdecks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    deck_id = Column(Integer, ForeignKey("decks.id"))  # Chave estrangeira para decks
    creation_date = Column(DateTime)

    deck = relationship("DeckEntity", back_populates="subdecks")
    cards = relationship("CardEntity", back_populates="subdecks")
    subdeck_user = relationship("UserSubDeckEntity", back_populates="subdeck")
