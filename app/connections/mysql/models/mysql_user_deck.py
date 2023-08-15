from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.connections.mysql.mysql_base import Base


class MySQLUserDeck(Base):
    __tablename__ = "users_deck"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    deck_id = Column(Integer, ForeignKey("decks.id"))
    creation_date = Column(DateTime)

    user = relationship("MySQLUser", back_populates="deck_user")
    deck = relationship("MySQLDeck", back_populates="deck_user")
