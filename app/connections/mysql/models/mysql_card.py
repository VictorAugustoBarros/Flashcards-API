from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.connections.mysql.models.mysql_base import Base


class MySQLCard(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    question = Column(String(255))
    answer = Column(String(255))
    subdeck_id = Column(
        Integer, ForeignKey("subdecks.id")
    )  # Chave estrangeira para decks
    creation_date = Column(DateTime)

    subdecks = relationship("MySQLSubDeck", back_populates="cards")
