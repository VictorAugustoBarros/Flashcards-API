from sqlalchemy.ext.declarative import declarative_base

from .card_entity import CardEntity
from .deck_entity import DeckEntity
from .subdeck_entity import SubDeckEntity
from .user_entity import UserEntity
from .subdeck_review_entity import SubDeckReviewEntity
from .review_difficulties_entity import ReviewDifficultiesEntity

Base = declarative_base()
