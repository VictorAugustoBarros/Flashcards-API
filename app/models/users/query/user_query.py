"""Card Query GraphQL."""
from typing import List

from ariadne import QueryType

from app.connections.dependencies import Dependencies
from app.controllers.user_controller import UserController
from app.models.responses.response import Response
from app.models.users.user import User
from app.utils.errors import DatabaseQueryFailed

user_query = QueryType()
db_conn = Dependencies.create_database()
user_controller = UserController(db_conn=db_conn)


@user_query.field("get_user")
def resolve_get_users(*_, user_id: int) -> User:
    """Busca de um usuário pelo ID

    Args:
        *_:
        user_id: ID do usuário

    Returns:
        User
    """
    try:
        return user_controller.get_user(user_id=user_id)

    except Exception as error:
        raise error


@user_query.field("get_users")
def resolve_get_users(*_) -> List[User]:
    """Busca dos usuários cadastrados

    Args:
        *_:

    Returns:
        List[User]: Lista com os usuários cadastrados
    """
    try:
        return user_controller.get_all_users()

    except Exception as error:
        raise error


@user_query.field("validate_username")
def resolve_validate_username(*_, username: str) -> Response:
    """Função para validar se o username já foi cadastrado

    Args:
        *_:
        username: Username do usuário

    Returns:
        Response
    """
    try:
        username = user_controller.validate_username_exists(username=username)
        if username:
            return Response(success=False, message="Username já existe!")

        return Response(success=True, message="Username disponível!")

    except DatabaseQueryFailed:
        return Response(success=False, message="Falha ao buscar User!")

    except Exception as error:
        raise error
