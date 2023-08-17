from unittest import TestCase
from unittest.mock import Mock

from app.connections.dependencies import Dependencies
from app.connections.mysql import MySQLUser
from app.controllers.user_controller import UserController
from app.models.users.user import User
from app.utils.errors import (
    DatabaseInsertFailed,
    DatabaseQueryFailed,
    DatabaseDeleteFailed,
)


class TestUserController(TestCase):
    """Classe para testes unitário da classe UserController"""

    db_conn = None

    @classmethod
    def setUp(self) -> None:
        """Método executado a cada teste"""
        self.db_conn = Dependencies.create_database()
        self.user_controller = UserController(db_conn=self.db_conn)

    def test_insert_user(self):
        """Teste de inserção de um novo usuário"""
        user = User(username="Teste", email="teste@teste", password="teste123")
        user_inserted = self.user_controller.insert_user(user=user)

        self.assertIsNotNone(user_inserted.id)

        self.user_controller.delete_user(user_id=user_inserted.id)

    def test_insert_error(self):
        """Teste de falha na inserção de um novo usuário"""
        self.user_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseInsertFailed):
            user = User(username="Teste", email="teste@teste", password="teste123")
            self.user_controller.insert_user(user=user)

    def test_validate_user_exists_true(self):
        """Teste de validação para User existente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = True
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        user_exists = self.user_controller.validate_user_exists(user_id=1)

        self.assertTrue(user_exists)

    def test_validate_user_exists_false(self):
        """Teste de validação para User inexistente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = False
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        user_exists = self.user_controller.validate_user_exists(user_id=1)

        self.assertFalse(user_exists)

    def test_validate_user_exists_error(self):
        """Teste de falha na validação se um User existe"""
        self.user_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.user_controller.validate_user_exists(user_id=1)

    def test_validate_user_email_username_exists_true(self):
        """Teste de validação para User existente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = True
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        user_exists = self.user_controller.validate_user_email_username_exists(
            username="teste", email="teste@teste"
        )

        self.assertTrue(user_exists)

    def test_validate_user_email_username_exists_false(self):
        """Teste de validação para User existente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = False
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        user_exists = self.user_controller.validate_user_email_username_exists(
            username="teste", email="teste@teste"
        )

        self.assertFalse(user_exists)

    def test_validate_user_email_username_exists_error(self):
        """Teste de falha na validação se um User existe"""
        self.user_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.user_controller.validate_user_email_username_exists(
                username="teste", email="teste@teste"
            )

    def test_validate_username_exists_true(self):
        """Teste de validação para Username existente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = True
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        user_exists = self.user_controller.validate_username_exists(username="teste")

        self.assertTrue(user_exists)

    def test_validate_username_exists_false(self):
        """Teste de validação para Username inexistente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = False
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        user_exists = self.user_controller.validate_username_exists(username="teste")

        self.assertFalse(user_exists)

    def test_validate_username_exists_error(self):
        """Teste de falha na validação se um Username existe"""
        self.user_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.user_controller.validate_username_exists(username="teste")

    def test_get_user_success(self):
        """Teste de busca de um User"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = MySQLUser(
            id=123123, username="teste", email="teste@teste"
        )

        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        user = self.user_controller.get_user(user_id=123123)

        self.assertEqual(user.id, 123123)

    def test_get_deck_none(self):
        """Teste de busca de um Deck"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = None

        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        user = self.user_controller.get_user(user_id=123123)

        self.assertIsNone(user)

    def test_get_deck_error(self):
        """Teste de falha na busca de um Deck pelo Deck ID"""
        self.user_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.user_controller.get_user(user_id=123123)

    def test_get_all_users(self):
        """Teste da busca de todos os Users cadastrados no banco"""
        mock_query = Mock()
        mock_session = Mock()

        mock_query.all.return_value = [
            MySQLUser(id=123, username="teste1", email="teste1@teste"),
            MySQLUser(id=1234, username="teste2", email="teste2@teste"),
            MySQLUser(id=12345, username="teste3", email="teste3@teste"),
        ]

        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        users = self.user_controller.get_all_users()

        self.assertEqual(users[0].id, 123)
        self.assertEqual(users[1].id, 1234)
        self.assertEqual(users[2].id, 12345)

    def test_get_all_users_error(self):
        """Teste de falha na busca de todos os SubDecks cadastrados no banco"""
        self.user_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseQueryFailed):
            self.user_controller.get_all_users()

    def test_delete_user(self):
        """Teste de falha da deleção de um User"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = True
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        mock_session.delete.return_value = True
        mock_session.commit.return_value = True

        self.user_controller.database.session = Mock(return_value=mock_session)

        subdeck_deleted = self.user_controller.delete_user(user_id=123)
        self.assertTrue(subdeck_deleted)

    def test_delete_subdeck_not_found(self):
        """Teste de falha da deleção de um Deck inexistente"""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session = Mock()

        mock_filter.first.return_value = None
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        self.user_controller.database.session = Mock(return_value=mock_session)

        subdeck_deleted = self.user_controller.delete_user(user_id=123)
        self.assertFalse(subdeck_deleted)

    def test_delete_subdeck_error(self):
        """Teste de falha da deleção de um Deck"""
        self.user_controller.database.session = Mock(
            side_effect=Exception("Simulating an error")
        )

        with self.assertRaises(DatabaseDeleteFailed):
            self.user_controller.delete_user(user_id=123)
