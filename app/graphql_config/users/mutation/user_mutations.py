"""Card Mutations GraphQL."""
import sentry_sdk
from ariadne import MutationType

from app.connections.mysql import MySQLDB
from app.graphql_config.models.response import Response
from app.models.user import User
from services.user_service import UserService

user_mutation = MutationType()


@user_mutation.field("add_user")
def resolve_add_user(_, info, email: str, username: str, password: str) -> Response:
    try:
        user_service = UserService(session=MySQLDB().session)
        user_inserted = user_service.create_user(user=User(
            email=email,
            username=username,
            password=password
        ))
        if not user_inserted:
            return Response(
                success=False, message="Falha ao criar User, informações inválidas!"
            )

        return Response(success=True, message="User criado com sucesso!")

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=True, message="Falha ao criar User!")
