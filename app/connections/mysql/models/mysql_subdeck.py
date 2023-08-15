"""MySQL SubDeck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.connections.mysql.mysql_base import Base


class MySQLSubDeck(Base):
    """Classe modelo do SQLAlchemy da tabela subdecks"""

    __tablename__ = "subdecks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    deck_id = Column(Integer, ForeignKey("decks.id"))  # Chave estrangeira para decks
    creation_date = Column(DateTime)

    deck = relationship("MySQLDeck", back_populates="subdecks")
    cards = relationship("MySQLCard", back_populates="subdecks")
    subdeck_user = relationship("MySQLUserSubDeck", back_populates="subdeck")
