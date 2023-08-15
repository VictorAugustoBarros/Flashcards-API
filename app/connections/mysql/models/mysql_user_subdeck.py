from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.connections.mysql.mysql_base import Base


class MySQLUserSubDeck(Base):
    __tablename__ = "users_subdeck"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subdeck_id = Column(Integer, ForeignKey("subdecks.id"))
    creation_date = Column(DateTime)

    user = relationship("MySQLUser", back_populates="subdeck_user")
    subdeck = relationship("MySQLSubDeck", back_populates="subdeck_user")
