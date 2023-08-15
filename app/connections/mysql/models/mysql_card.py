"""MySQL User SubDeck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.connections.mysql.mysql_base import Base


class MySQLCard(Base):
    """Classe modelo do SQLAlchemy da tabela cards"""

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    question = Column(String(255))
    answer = Column(String(255))
    subdeck_id = Column(Integer, ForeignKey("subdecks.id"))
    creation_date = Column(DateTime)

    subdecks = relationship("MySQLSubDeck", back_populates="cards")
