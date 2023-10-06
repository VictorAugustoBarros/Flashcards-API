"""MySQL Users model."""
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class UserEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela users"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    deck = relationship("DeckEntity", back_populates="user")
