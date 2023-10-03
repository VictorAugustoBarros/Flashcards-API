"""Card Mutations GraphQL."""
import sentry_sdk
from ariadne import MutationType

from app.connections.mysql import MySQLDB
from app.graphql_config.models.response import Response
from app.models.user import User
from app.utils.errors import TokenError
from services.user_service import UserService
from app.validations.middleware_validation import validate_token

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


@user_mutation.field("edit_user")
@validate_token
def resolve_edit_user(_, info, email: str, username: str, password: str, token: dict) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        user_info = token["user_info"]

        user_service = UserService(session=MySQLDB().session)
        user_updated = user_service.update_user(user=User(
            id=user_info["id"],
            email=email,
            username=username,
            password=password
        ))
        if not user_updated:
            return Response(
                success=False, message="Falha ao alterado User, informações inválidas!"
            )

        return Response(success=True, message="User alterado com sucesso!")

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=True, message="Falha ao alterado User!")


@user_mutation.field("delete_user")
@validate_token
def resolve_delete_user(_, info, token: dict) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        user_info = token["user_info"]

        user_service = UserService(session=MySQLDB().session)
        user_deleted = user_service.delete_user(user_id=user_info["id"])
        if not user_deleted:
            return Response(
                success=False, message="Falha ao deletar User!"
            )

        return Response(success=True, message="User deletado com sucesso!")

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=True, message="Falha ao deletar User!")
