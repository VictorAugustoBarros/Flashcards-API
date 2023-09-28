"""Card Repository."""
from repository.base_repository import BaseRepository


class CardRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()

    def get_cards_user(self):
        ...
