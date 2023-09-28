"""MySQL User Deck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class UserDeckEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela users_deck"""

    __tablename__ = "users_deck"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    deck_id = Column(Integer, ForeignKey("decks.id"))
    creation_date = Column(DateTime)

    user = relationship("UserEntity", back_populates="deck_user")
    deck = relationship("DeckEntity", back_populates="deck_user")
