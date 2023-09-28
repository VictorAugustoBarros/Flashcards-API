from sqlalchemy.ext.declarative import declarative_base

from .card_entity import CardEntity
from .deck_entity import DeckEntity
from .subdeck_entity import SubDeckEntity
from .user_entity import UserEntity
from .user_deck_entity import UserDeckEntity
from .user_subdeck_entity import UserSubDeckEntity

Base = declarative_base()
