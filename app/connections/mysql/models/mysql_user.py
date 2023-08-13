from sqlalchemy import Column, DateTime, Integer, String

from app.connections.mysql.models.mysql_base import Base


class MySQLUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    creation_date = Column(DateTime)
