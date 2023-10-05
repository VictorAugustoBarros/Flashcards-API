from sqlalchemy.ext.declarative import declarative_base

from .card_entity import CardEntity
from .deck_entity import DeckEntity
from .subdeck_entity import SubDeckEntity
from .user_entity import UserEntity
from .subdeck_review_entity import SubDeckReviewEntity
from .review_difficulties_entity import ReviewDifficultiesEntity
from .review_difficulties_interval_time_entity import ReviewDifficultiesIntervalTimeEntity

Base = declarative_base()
