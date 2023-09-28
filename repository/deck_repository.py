"""Deck Repository."""
from repository.base_repository import AbstractRepository


class DeckRepository(AbstractRepository):
    def add(self):
        print("deck add...")
        ...

    def remove(self):
        print("deck remove...")
        ...

    def update(self):
        print("deck update...")
        ...
