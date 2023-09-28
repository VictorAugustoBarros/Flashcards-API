"""MySQL User SubDeck model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class UserSubDeckEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela users_subdeck"""

    __tablename__ = "users_subdeck"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subdeck_id = Column(Integer, ForeignKey("subdecks.id"))
    creation_date = Column(DateTime)

    user = relationship("UserEntity", back_populates="subdeck_user")
    subdeck = relationship("SubDeckEntity", back_populates="subdeck_user")
