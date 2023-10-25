"""Card Mutations GraphQL."""
import sentry_sdk
from ariadne import MutationType

from app.connections.mysql import MySQLDB
from app.models.card import Card
from app.services import CardService
from app.graphql_config.models.card_response import CardResponse
from app.graphql_config.models.response import Response
from app.utils.errors import DatabaseInsertFailed, TokenError
from app.utils.middleware_validation import validate_token
from app.services.subdeck_service import SubdeckService

card_mutations = MutationType()


@card_mutations.field("add_card")
@validate_token
def resolve_add_card(
    _, info, subdeck_id: int, question: str, answer: str, token: dict
) -> CardResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        mysql_session = MySQLDB().session
        subdeck_service = SubdeckService(session=mysql_session)
        subdeck_user = subdeck_service.validate_subdeck_user(
            user_id=user_info["id"], subdeck_id=subdeck_id
        )
        if not subdeck_user:
            return CardResponse(
                response=Response(success=False, message="SubDeck não encontrado!")
            )

        card_service = CardService(session=mysql_session)
        card = card_service.create_card(
            card=Card(question=question, answer=answer, subdeck_id=subdeck_id)
        )
        if not card:
            return CardResponse(
                response=Response(
                    success=False, message="Falha ao criar Card, informações inválidas!"
                )
            )

        return CardResponse(
            card=card,
            response=Response(success=True, message="Card criado com sucesso!"),
        )

    except TokenError as error:
        return CardResponse(response=Response(success=False, message=str(error)))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return CardResponse(
            response=Response(success=True, message="Falha ao criar Card!")
        )


@card_mutations.field("edit_card")
@validate_token
def resolve_edit_card(
    _, info, card_id: int, question: str, answer: str, token: dict
) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        card_service = CardService(session=MySQLDB().session)
        card_user = card_service.validate_card_user(
            user_id=user_info["id"], card_id=card_id
        )
        if not card_user:
            return Response(success=False, message="Card não encontrado!")

        card_service.update_card(
            card_id=card_id, card=Card(question=question, answer=answer)
        )
        return Response(success=True, message="Card atualizado com sucesso!")

    except DatabaseInsertFailed:
        return Response(success=False, message="Falha ao atualizar Card!")

    except TokenError as error:
        return Response(success=False, message=str(error))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=True, message="Falha ao atualizar Card!")


@card_mutations.field("delete_card")
@validate_token
def resolve_delete_card(_, info, card_id: int, token: dict) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        card_service = CardService(session=MySQLDB().session)
        card_user = card_service.validate_card_user(
            user_id=user_info["id"], card_id=card_id
        )
        if not card_user:
            return Response(success=False, message="Card não encontrado!")

        card_service.delete_card(card_id=card_id)

        return Response(success=True, message="Card removido com sucesso!")

    except DatabaseInsertFailed:
        return Response(success=False, message="Falha ao remover Card!")

    except TokenError as error:
        return Response(success=False, message=str(error))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=True, message="Falha ao remover Card!")
