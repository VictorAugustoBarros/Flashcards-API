"""MySQL ReviewDifficultiesIntervalTimeEntity model."""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from entities.base_entity import mysql_base


class ReviewDifficultiesIntervalTimeEntity(mysql_base):
    """Classe modelo do SQLAlchemy da tabela review_difficulties_interval_time"""

    __tablename__ = "review_difficulties_interval_time"

    id = Column(Integer, primary_key=True)
    minutes = Column(Integer)
    review_difficulties_id = Column(Integer, ForeignKey("review_difficulties.id"))

    review_difficulties = relationship(
        "ReviewDifficultiesEntity", back_populates="review_difficulties_interval_time"
    )
