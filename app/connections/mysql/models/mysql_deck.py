"""MySQL Deck model."""
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.connections.mysql.mysql_base import Base


class MySQLDeck(Base):
    """Classe modelo do SQLAlchemy da tabela decks"""

    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    creation_date = Column(DateTime)

    subdecks = relationship("MySQLSubDeck", back_populates="deck")
    deck_user = relationship("MySQLUserDeck", back_populates="deck")
