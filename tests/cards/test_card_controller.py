from unittest import TestCase
from unittest.mock import Mock
from app.services.card_service import CardService
from app.services.subdeck_service import SubdeckService
from app.services.deck_service import DeckService
from app.models.card import Card
from app.models.deck import Deck
from app.models.subdeck import SubDeck
from app.connections.mysql import MySQLDB
from app.utils.errors import DatabaseInsertFailed, DatabaseQueryFailed


class TestCardController(TestCase):
    """Classe para testes unitário da classe CardController"""

    mysql_session = None
    deck_service = None
    subdeck_service = None
    card_service = None

    @classmethod
    def setUp(self) -> None:
        """Método executado a cada teste"""
        mysql_session = MySQLDB().session
        self.deck_service = DeckService(session=mysql_session)
        self.subdeck_service = SubdeckService(session=mysql_session)
        self.card_service = CardService(session=mysql_session)

    def test_insert_card(self):
        """Teste de inserção de um card no banco de dados"""
        # Criação dos dados
        deck = Deck(name="Deck Teste", description="Deck para Teste")
        deck_inserted = self.deck_service.create_deck(deck=deck)

        subdeck = SubDeck(name="SubDeck Teste", description="Subdeck para testes", deck_id=deck_inserted.id)
        subdeck_inserted = self.subdeck_service.create_subdeck(
            subdeck=subdeck
        )

        card = Card(question="Teste", subdeck_id=subdeck_inserted.id, answer="Teste")
        card_inserted = self.card_service.create_card(
            card=card
        )

        # Testes
        self.assertIsNotNone(card_inserted.id)

        # Remoção dos dados
        self.deck_service.delete_deck(deck_id=deck.id)
        self.subdeck_service.delete_subdeck(subdeck_id=subdeck.id)
        self.card_service.delete_card(card_id=card.id)

    def test_insert_card_subdeck_not_exists(self):
        """Teste de inserção de um card informando um subdeck_id inexistente"""
        card = Card(question="Teste", answer="Teste")

        with self.assertRaises(DatabaseInsertFailed):
            self.card_controller.insert_card(card=card, subdeck_id=128937)

    def test_delete_card_not_exists(self):
        """Teste de deleção de um card inexistente"""
        with self.assertRaises(DatabaseInsertFailed):
            self.card_controller.delete_card(card_id=12312312)

    def test_get_all_cards(self):
        """Teste da busca de todos os Cards cadastrados no banco"""
        mock_query = Mock()
        mock_session = Mock()
        mock_session.query.return_value = mock_query

        mock_query.all.return_value = [
            Card(question="Teste1", answer="Teste1"),
            Card(question="Teste2", answer="Teste2"),
        ]

        self.card_controller.database.session = Mock(return_value=mock_session)

        cards = self.card_controller.get_all_cards()

        self.assertIsInstance(cards, list)
        self.assertEqual(len(cards), 2)

    def test_get_all_cards_error(self):
        """Teste de falha da busca de todos os Cards cadastrados no banco"""
        self.card_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.card_controller.get_all_cards()

    def test_get_card_return_card(self):
        mock_filter = Mock()
        mock_query = Mock()
        mock_session = Mock()

        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        # Configurar os encadeamentos de chamadas
        mock_filter.first.return_value = Card(
            question="PeruntaTeste", answer="RespostaTeste"
        )

        # Substituir temporariamente o método sessionmaker().session
        self.card_controller.database.session = Mock(return_value=mock_session)

        # Chamar a função e verificar o retorno
        card = self.card_controller.get_card(card_id=1)
        self.assertIsInstance(card, Card)
        self.assertEqual(card.question, "PeruntaTeste")
        self.assertEqual(card.answer, "RespostaTeste")

    def test_get_card_return_none(self):
        mock_filter = Mock()
        mock_query = Mock()
        mock_session = Mock()

        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        # Configurar os encadeamentos de chamadas
        mock_filter.first.return_value = None

        # Substituir temporariamente o método sessionmaker().session
        self.card_controller.database.session = Mock(return_value=mock_session)

        # Chamar a função e verificar o retorno
        card = self.card_controller.get_card(card_id=1)
        self.assertIsNone(card)

    def test_get_card_error(self):
        """Teste de falha da busca de todos os Cards cadastrados no banco"""
        self.card_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.card_controller.get_card(card_id=1)
