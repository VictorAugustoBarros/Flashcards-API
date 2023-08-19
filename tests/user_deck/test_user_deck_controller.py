from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from app.connections.dependencies import Dependencies
from app.connections.mysql import MySQLUserDeck, MySQLDeck
from app.controllers.deck_controller import DeckController
from app.controllers.user_controller import UserController
from app.controllers.user_deck_controller import UserDeckController
from app.models.decks.deck import Deck
from app.models.users.user import User
from app.utils.errors import (
    DatabaseInsertFailed,
    DatabaseQueryFailed,
    DatabaseDeleteFailed,
)


class TestUserDeckController(TestCase):
    """Classe para testes unitário da classe UserDeckController"""

    db_conn = None

    @classmethod
    def setUp(self) -> None:
        """Método executado a cada teste"""
        self.db_conn = Dependencies.create_database()
        self.user_controller = UserController(db_conn=self.db_conn)
        self.user_deck_controller = UserDeckController(db_conn=self.db_conn)
        self.deck_controller = DeckController(db_conn=self.db_conn)

    def test_insert_user_deck(self):
        """Teste de inserção do vinculo entre um User e um Deck"""
        user = User(username="Teste", email="teste@teste", password="teste123")
        user_inserted = self.user_controller.insert_user(user=user)

        deck = Deck(name="Deck Teste", description="Deck para Teste")
        deck_inserted = self.deck_controller.insert_deck(deck=deck)

        user_deck_inserted = self.user_deck_controller.insert_user_deck(
            user_id=user_inserted.id, deck_id=deck_inserted.id
        )

        self.assertIsNotNone(user_deck_inserted.id)

        self.user_controller.delete_user(user_id=user_inserted.id)
        self.deck_controller.delete_deck(deck_id=deck_inserted.id)
        self.user_deck_controller.delete_user_deck(user_deck_id=user_deck_inserted.id)

    def test_insert_user_deck_error(self):
        """Teste de falha na inserção do vinculo entre um User e um Deck"""
        self.user_deck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseInsertFailed):
            self.user_deck_controller.insert_user_deck(user_id=1, deck_id=1)

    def test_get_user_deck(self):
        """Teste de busca dos Deck vinculados a um User"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.all.return_value = [
            MySQLUserDeck(
                id=1234,
                user_id=1,
                deck_id=1,
                creation_date=datetime.now(),
                deck=MySQLDeck(id=1),
            )
        ]

        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_deck_controller.database.session = Mock(return_value=mock_session)

        self.user_deck_controller.deck_controller.get_deck = Mock(
            return_value=Deck(id=123213, name="Deck1", description="Deck1")
        )

        decks = self.user_deck_controller.get_user_deck(user_id=1)

        self.assertEqual(decks[0].id, 123213)

    def test_get_user_deck_error(self):
        """Teste de falha na busca de um Deck pelo Deck ID"""
        self.user_deck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.user_deck_controller.get_user_deck(user_id=1)

    def test_validate_link_userdeck_exists_true(self):
        """Teste de validação do vinculo entre um User e um Deck existente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = True
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_deck_controller.database.session = Mock(return_value=mock_session)

        user_deck_exists = self.user_deck_controller.validate_link_userdeck_exists(
            user_id=1, deck_id=1
        )

        self.assertTrue(user_deck_exists)

    def test_validate_link_userdeck_exists_false(self):
        """Teste de validação do vinculo entre um User e um Deck inexistente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = False
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_deck_controller.database.session = Mock(return_value=mock_session)

        user_deck_exists = self.user_deck_controller.validate_link_userdeck_exists(
            user_id=1, deck_id=1
        )

        self.assertFalse(user_deck_exists)

    def test_validate_link_userdeck_exists_error(self):
        """Teste de falha na validação se um Deck existe"""
        self.user_deck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.user_deck_controller.validate_link_userdeck_exists(
                user_id=1, deck_id=1
            )

    def test_delete_user_deck(self):
        """Teste de deleção do vinculo entre um User e um Deck existente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        mock_filter.first.return_value = True

        mock_session.delete.return_value = True
        mock_session.commit.return_value = True

        self.user_deck_controller.database.session = Mock(return_value=mock_session)

        user_deck_deleted = self.user_deck_controller.delete_user_deck(user_deck_id=123)
        self.assertTrue(user_deck_deleted)

    def test_delete_deck_not_found(self):
        """Teste de falha na deleção do vinculo entre um User e um Deck inexistente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        mock_filter.first.return_value = False

        mock_session.delete.return_value = True
        mock_session.commit.return_value = True

        self.user_deck_controller.database.session = Mock(return_value=mock_session)

        user_deck_deleted = self.user_deck_controller.delete_user_deck(user_deck_id=123)
        self.assertFalse(user_deck_deleted)

    def test_delete_deck_error(self):
        """Teste de falha na deleção do vinculo entre um User e um Deck"""
        self.user_deck_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseDeleteFailed):
            self.user_deck_controller.delete_user_deck(user_deck_id=123)
