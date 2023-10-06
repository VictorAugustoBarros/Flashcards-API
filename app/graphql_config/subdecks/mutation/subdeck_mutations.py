"""SubDeckMutations GraphQL."""
import sentry_sdk
from ariadne import MutationType

from app.connections.mysql import MySQLDB
from app.models.subdeck import SubDeck
from services.subdeck_service import SubdeckService
from app.graphql_config.models.subdeck_response import SubDeckResponse
from app.graphql_config.models.response import Response
from app.utils.errors import DatabaseInsertFailed, TokenError
from app.validations.middleware_validation import validate_token

subdeck_mutations = MutationType()


@subdeck_mutations.field("add_subdeck")
@validate_token
def resolve_add_subdeck(_, info, deck_id: int, name: str, description: str, token: dict) -> SubDeckResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        subdeck_service = SubdeckService(session=MySQLDB().session)
        subsubdeck = subdeck_service.create_subdeck(
            subdeck=SubDeck(
                deck_id=deck_id,
                name=name,
                description=description
            )
        )
        if not subsubdeck:
            return SubDeckResponse(
                response=Response(
                    success=False, message="Falha ao criar SubDeck, informações inválidas!"
                )
            )

        return SubDeckResponse(
            subdeck=subsubdeck,
            response=Response(success=True, message="SubDeck criado com sucesso!"),
        )

    except DatabaseInsertFailed:
        return SubDeckResponse(
            response=Response(success=False, message="Falha ao criar SubDeck!")
        )

    except TokenError as error:
        return SubDeckResponse(response=Response(success=False, message=str(error)))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return SubDeckResponse(response=Response(success=True, message="Falha ao remover SubDeck!"))


@subdeck_mutations.field("edit_subdeck")
@validate_token
def resolve_edit_subdeck(_, info, subdeck_id: int, name: str, description: str, token: dict) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        subdeck_service = SubdeckService(session=MySQLDB().session)
        subdeck_user = subdeck_service.validate_subdeck_user(user_id=user_info["id"], subdeck_id=subdeck_id)
        if not subdeck_user:
            return Response(success=False, message="SubDeck não encontrado!")

        subdeck_service.update_subdeck(
            subdeck_id=subdeck_id,
            subdeck=SubDeck(
                name=name,
                description=description
            )
        )
        return Response(success=True, message="SubDeck atualizado com sucesso!")

    except DatabaseInsertFailed:
        return Response(success=False, message="Falha ao atualizar SubDeck!")

    except TokenError as error:
        return Response(success=False, message=str(error))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=True, message="Falha ao remover SubDeck!")


