from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from app.connections.dependencies import Dependencies
from app.connections.mysql import MySQLDeck, MySQLSubDeck, MySQLCard
from app.controllers.deck_controller import DeckController
from app.models.decks.deck import Deck
from app.models.subdecks.subdeck import SubDeck
from app.utils.errors import (
    DatabaseInsertFailed,
    DatabaseDeleteFailed,
    DatabaseQueryFailed,
)


class TestDeckController(TestCase):
    """Classe para testes unitário da classe DeckController"""

    db_conn = None
    deck_controller = None

    @classmethod
    def setUp(self) -> None:
        """Método executado a cada teste"""
        self.db_conn = Dependencies.create_database()
        self.deck_controller = DeckController(db_conn=self.db_conn)

    def test_insert_deck(self):
        """Teste de inserção de um Deck no banco de dados"""
        deck = Deck(name="Deck Teste", description="Deck para Teste")
        deck_inserted = self.deck_controller.insert_deck(deck=deck)

        self.assertIsNotNone(deck_inserted.id)

        self.deck_controller.delete_deck(deck_id=deck.id)

    def test_insert_deck_error(self):
        """Teste de falha da inserção de um Deck"""
        self.deck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseInsertFailed):
            deck = Deck(name="Deck Teste", description="Deck para Teste")
            self.deck_controller.insert_deck(deck=deck)

    def test_delete_deck(self):
        """Teste de falha da deleção de um Deck"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        mock_filter.first.return_value = True

        mock_session.delete.return_value = True
        mock_session.commit.return_value = True

        self.deck_controller.database.session = Mock(return_value=mock_session)

        deck_deleted = self.deck_controller.delete_deck(deck_id=43546)
        self.assertTrue(deck_deleted)

    def test_delete_deck_not_found(self):
        """Teste de falha da deleção de um Deck inexistente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = None
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.deck_controller.database.session = Mock(return_value=mock_session)

        deck_deleted = self.deck_controller.delete_deck(deck_id=43546)
        self.assertFalse(deck_deleted)

    def test_delete_deck_error(self):
        """Teste de falha da deleção de um Deck"""
        self.deck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseDeleteFailed):
            self.deck_controller.delete_deck(deck_id=43546)

    def test_get_all_decks(self):
        """Teste da busca de todos os Decks cadastrados no banco"""
        mock_query = Mock()
        mock_options = Mock()
        mock_session = Mock()
        mock_subdecks = Mock()

        mock_options.all.return_value = [
            MySQLDeck(
                id=1,
                name="Deck1",
                description="Description1",
                creation_date=datetime.now(),
            ),
            MySQLDeck(
                id=2,
                name="Deck2",
                description="Description2",
                creation_date=datetime.now(),
            ),
            MySQLDeck(
                id=3,
                name="Deck3",
                description="Description3",
                creation_date=datetime.now(),
            ),
        ]

        # mock_options.joinedload.return_value = mock_joinedload
        mock_query.options.return_value = mock_options
        mock_session.query.return_value = mock_query

        self.deck_controller.database.session = Mock(return_value=mock_session)

        mock_subdecks.return_value = [
            SubDeck(name="SubDeck1", description="Description1")
        ]

        self.deck_controller.map_subdecks_and_cards = Mock(return_value=mock_subdecks)

        decks = self.deck_controller.get_all_decks()

        self.assertIsInstance(decks, list)
        self.assertEqual(len(decks), 3)

    def test_get_all_decks_error(self):
        """Teste de falha da busca de todos os Decks"""
        self.deck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.deck_controller.get_all_decks()

    def test_validate_deck_exists_true(self):
        """Teste de validação para Deck existente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = True
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.deck_controller.database.session = Mock(return_value=mock_session)

        deck_exists = self.deck_controller.validate_deck_exists(deck_id=1)

        self.assertTrue(deck_exists)

    def test_validate_deck_exists_false(self):
        """Teste de validação para Deck inexistente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = False
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.deck_controller.database.session = Mock(return_value=mock_session)

        deck_exists = self.deck_controller.validate_deck_exists(deck_id=1)

        self.assertFalse(deck_exists)

    def test_validate_deck_exists_error(self):
        """Teste de falha na validação se um Deck existe"""
        self.deck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.deck_controller.validate_deck_exists(deck_id=1)

    def test_get_deck_success(self):
        """Teste de busca de um Deck"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_options = Mock()
        mock_session = Mock()
        mock_subdecks = Mock()

        mock_options.first.return_value = MySQLDeck(
            id=112313,
            name="Deck1",
            description="Description1",
            creation_date=datetime.now(),
        )

        # mock_options.joinedload.return_value = mock_joinedload
        mock_filter.options.return_value = mock_options
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.deck_controller.database.session = Mock(return_value=mock_session)

        mock_subdecks.return_value = [
            SubDeck(name="SubDeck1", description="Description1")
        ]

        self.deck_controller.map_subdecks_and_cards = Mock(return_value=mock_subdecks)

        deck = self.deck_controller.get_deck(deck_id=112313)

        self.assertEqual(deck.id, 112313)

    def test_get_deck_none(self):
        """Teste de busca de um Deck"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_options = Mock()
        mock_session = Mock()

        mock_options.first.return_value = None

        mock_filter.options.return_value = mock_options
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.deck_controller.database.session = Mock(return_value=mock_session)

        deck = self.deck_controller.get_deck(deck_id=112313)

        self.assertIsNone(deck)

    def test_get_deck_error(self):
        """Teste de falha na busca de um Deck pelo Deck ID"""
        self.deck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.deck_controller.get_deck(deck_id=1)

    def test_map_subdecks_and_cards(self):
        """Teste de falha no mapeamento dos SubDecks e Cards"""
        subdeck_cards = self.deck_controller.map_subdecks_and_cards(
            [MySQLSubDeck(id=1, cards=[MySQLCard(id=123)])]
        )

        self.assertEqual(subdeck_cards[0].id, 1)
        self.assertEqual(subdeck_cards[0].cards[0].id, 123)
