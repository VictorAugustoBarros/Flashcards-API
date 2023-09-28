"""Card Query GraphQL."""
import sentry_sdk

from ariadne import QueryType
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from app.connections.mysql import MySQLDB
from app.graphql_config.models.response import Response
from app.graphql_config.models.user_login_response import UserLoginResponse
from app.graphql_config.models.user_response import UserResponse
from app.models.user import User
from app.jwt_manager import JwtManager
from app.utils.errors import DatabaseQueryFailed
from services.user_service import UserService

user_query = QueryType()


@user_query.field("get_user")
def resolve_get_users(*_, user_id: int) -> UserResponse:
    """Busca de um usuário pelo ID

    Args:
        *_:
        user_id: ID do usuário

    Returns:
        User
    """
    try:
        user_service = UserService(session=MySQLDB().session)
        user = user_service.get_user(user_id=user_id)
        if not user:
            return UserResponse(response=Response(success=False, message="User não encontrado!"))

        return UserResponse(user=user, response=Response(success=True))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return UserResponse(response=Response(success=False, message="Falha na busca do User!"))


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
        user_service = UserService(session=MySQLDB().session)
        username = user_service.validate_username(username=username)
        if username:
            return Response(success=False, message="Username já existe!")

        return Response(success=True, message="Username disponível!")

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=False, message="Falha ao verificar disponibilidade do Username!")


@user_query.field("login")
def resolve_login(*_, email: str, password: str) -> UserLoginResponse:
    """Função para validar login usuário

    Args:
        *_:
        email(str): Email do usuário
        password(str): Senha do usuário

    Returns:
        UserLoginResponse
    """
    try:
        user_service = UserService(session=MySQLDB().session)
        jwt_token = user_service.login(email=email, password=password)
        if not jwt_token:
            return UserLoginResponse(
                response=Response(success=False, message="Usuário ou Email inválido!")
            )

        return UserLoginResponse(
            jwt_token=jwt_token,
            response=Response(success=True, message="Usuário logado com sucesso!")
        )

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return UserLoginResponse(response=Response(success=False, message="Falha ao validar Login!"))
