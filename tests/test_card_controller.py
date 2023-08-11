from unittest import TestCase
from app.controllers.card_controller import CardController
from app.models.cards import Card


class TestCardController(TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.card_controller = CardController()

    @classmethod
    def tearDownClass(self) -> None:
        self.card_controller.database.close()

    def test_insert_card(self):
        card = Card(question="teste", answer="teste")
        print(self.card_controller.insert_card(card=card))
