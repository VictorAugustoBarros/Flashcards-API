from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from app.connections.dependencies import Dependencies
from app.connections.mysql import MySQLSubDeck, MySQLCard
from app.controllers.deck_controller import DeckController
from app.controllers.subdeck_controller import SubDeckController
from app.models.deck import Deck
from app.models.subdeck import SubDeck
from app.utils.errors import (
    DatabaseInsertFailed,
    DatabaseDeleteFailed,
    DatabaseQueryFailed,
)


class TestSubDeckController(TestCase):
    """Classe para testes unitário da classe DeckController"""

    db_conn = None

    @classmethod
    def setUp(self) -> None:
        """Método executado a cada teste"""
        self.db_conn = Dependencies.create_database()
        self.deck_controller = DeckController(db_conn=self.db_conn)
        self.subdeck_controller = SubDeckController(db_conn=self.db_conn)

    def test_insert_subdeck(self):
        """Teste de inserção de um SubDeck no banco de dados"""
        deck = Deck(name="Deck Teste", description="Deck para Teste")
        deck_inserted = self.deck_controller.insert_deck(deck=deck)

        subdeck = SubDeck(name="SubDeck1", description="SubDeck para Teste")
        subdeck_inserted = self.subdeck_controller.insert_subdeck(
            subdeck=subdeck, deck_id=deck_inserted.id
        )

        self.assertIsNotNone(subdeck_inserted.id)

        self.deck_controller.delete_deck(deck_id=deck.id)
        self.subdeck_controller.delete_subdeck(subdeck_id=subdeck_inserted.id)

    def test_insert_subdeck_error(self):
        """Teste de inserção de um SubDeck no banco de dados"""
        self.subdeck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseInsertFailed):
            subdeck = SubDeck(name="SubDeck1", description="SubDeck para Teste")
            self.subdeck_controller.insert_subdeck(subdeck=subdeck, deck_id=123)

    def test_delete_subdeck(self):
        """Teste de falha da deleção de um SubDeck"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = True
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        mock_session.delete.return_value = True
        mock_session.commit.return_value = True

        self.subdeck_controller.database.session = Mock(return_value=mock_session)

        subdeck_deleted = self.subdeck_controller.delete_subdeck(subdeck_id=43546)
        self.assertTrue(subdeck_deleted)

    def test_delete_subdeck_not_found(self):
        """Teste de falha da deleção de um Deck inexistente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = None
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.deck_controller.database.session = Mock(return_value=mock_session)

        subdeck_deleted = self.subdeck_controller.delete_subdeck(subdeck_id=43546)
        self.assertFalse(subdeck_deleted)

    def test_delete_subdeck_error(self):
        """Teste de falha da deleção de um Deck"""
        self.subdeck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseDeleteFailed):
            self.subdeck_controller.delete_subdeck(subdeck_id=43546)

    def test_get_all_subdecks(self):
        """Teste da busca de todos os SubDecks cadastrados no banco"""
        mock_query = Mock()
        mock_options = Mock()
        mock_session = Mock()
        mock_subdecks = Mock()

        mock_options.all.return_value = [
            MySQLSubDeck(
                id=1,
                name="SubDeck1",
                description="Description1",
                creation_date=datetime.now(),
                cards=[MySQLCard(id=1)],
            ),
            MySQLSubDeck(
                id=2,
                name="SubDeck2",
                description="Description2",
                creation_date=datetime.now(),
                cards=[MySQLCard(id=2)],
            ),
            MySQLSubDeck(
                id=3,
                name="SubDeck3",
                description="Description3",
                creation_date=datetime.now(),
                cards=[MySQLCard(id=3)],
            ),
        ]

        # mock_options.joinedload.return_value = mock_joinedload
        mock_query.options.return_value = mock_options
        mock_session.query.return_value = mock_query

        self.subdeck_controller.database.session = Mock(return_value=mock_session)

        subdecks = self.subdeck_controller.get_all_subdecks()

        self.assertEqual(subdecks[0].id, 1)
        self.assertEqual(subdecks[1].id, 2)
        self.assertEqual(subdecks[2].id, 3)

        self.assertEqual(subdecks[0].cards[0].id, 1)
        self.assertEqual(subdecks[1].cards[0].id, 2)
        self.assertEqual(subdecks[2].cards[0].id, 3)

    def test_get_all_subdecks_error(self):
        """Teste de falha na busca de todos os SubDecks cadastrados no banco"""
        self.subdeck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.subdeck_controller.get_all_subdecks()

    def test_get_subdeck_success(self):
        """Teste de busca de um SubDeck"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_options = Mock()
        mock_session = Mock()

        mock_options.first.return_value = MySQLSubDeck(
            id=12783612,
            name="SubDeck1",
            description="Description1",
            creation_date=datetime.now(),
            cards=[MySQLCard(id=11231, question="Teste1")],
        )

        mock_filter.options.return_value = mock_options
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.subdeck_controller.database.session = Mock(return_value=mock_session)

        subdeck = self.subdeck_controller.get_subdeck(subdeck_id=112313)

        self.assertEqual(subdeck.id, 12783612)
        self.assertEqual(subdeck.cards[0].id, 11231)

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

        self.subdeck_controller.database.session = Mock(return_value=mock_session)

        deck = self.subdeck_controller.get_subdeck(subdeck_id=112313)

        self.assertIsNone(deck)

    def test_get_deck_error(self):
        """Teste de falha na busca de um Deck pelo Deck ID"""
        self.subdeck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.subdeck_controller.get_subdeck(subdeck_id=112313)

    def test_validate_subdeck_exists_true(self):
        """Teste de validação para SubDeck existente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = True
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.subdeck_controller.database.session = Mock(return_value=mock_session)

        deck_exists = self.subdeck_controller.validate_subdeck_exists(subdeck_id=1)

        self.assertTrue(deck_exists)

    def test_validate_deck_exists_false(self):
        """Teste de validação para Deck inexistente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = False
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.subdeck_controller.database.session = Mock(return_value=mock_session)

        deck_exists = self.subdeck_controller.validate_subdeck_exists(subdeck_id=1)

        self.assertFalse(deck_exists)

    def test_validate_deck_exists_error(self):
        """Teste de falha na validação se um Deck existe"""
        self.subdeck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.subdeck_controller.validate_subdeck_exists(subdeck_id=1)
