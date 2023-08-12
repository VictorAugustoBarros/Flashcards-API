"""Deck Controller."""
from datetime import datetime

from app.dependencies import get_database
from app.errors import CreateCardError
from app.models.decks.decks import Deck


class DeckController:
    """Classe para gerenciamento dos Deck."""

    def __init__(self):
        """Construtor da classe."""
        self.database = get_database()
        self.collection = "Decks"

    def insert_deck(self, deck: Deck):
        """Inserção de um novo Deck.

        Args:
            deck (Deck): Deck a ser inserido

        Returns:
            inserted_id (int): ID do registro gerado pelo MongoDB
        """
        try:
            deck.creation_date = datetime.now()
            inserted_id = self.database.insert_document(
                collection_name=self.collection, document=deck.__dict__
            )
            return inserted_id

        except Exception as error:
            raise CreateCardError()

    def get_all_decks(self):
        """Busca de todos os Decks cadastrados.

        Returns:
            decks (list): Lista com todos os Decks
        """
        documents = self.database.find_documents(collection_name=self.collection)
        cards = []
        for document in documents:
            cards.append(
                {"question": document.get("question"), "answer": document.get("answer")}
            )

        if not cards:
            return None

        return cards
