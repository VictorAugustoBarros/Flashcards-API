from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.connections.mysql.models.mysql_base import Base


class MySQLDeck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    creation_date = Column(DateTime)

    subdecks = relationship("MySQLSubDeck", back_populates="deck")
