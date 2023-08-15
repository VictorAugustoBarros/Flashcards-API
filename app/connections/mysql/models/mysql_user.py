from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.connections.mysql.mysql_base import Base


class MySQLUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    creation_date = Column(DateTime)

    deck_user = relationship("MySQLUserDeck", back_populates="user")
    subdeck_user = relationship("MySQLUserSubDeck", back_populates="user")
