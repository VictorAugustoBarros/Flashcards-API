"""DeckMutations GraphQL."""
import sentry_sdk
from ariadne import MutationType

from app.connections.mysql import MySQLDB
from app.models.deck import Deck
from services.deck_service import DeckService
from app.graphql_config.models.deck_response import DeckResponse
from app.graphql_config.models.response import Response
from app.utils.errors import DatabaseInsertFailed, TokenError
from app.validations.middleware_validation import validate_token

deck_mutations = MutationType()


@deck_mutations.field("add_deck")
@validate_token
def resolve_add_deck(_, info, name: str, description: str, token: dict) -> DeckResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        deck_service = DeckService(session=MySQLDB().session)
        deck = deck_service.create_deck(
            deck=Deck(name=name, description=description, user_id=user_info["id"])
        )
        if not deck:
            return DeckResponse(
                response=Response(
                    success=False, message="Falha ao criar Deck, informações inválidas!"
                )
            )

        return DeckResponse(
            deck=deck,
            response=Response(success=True, message="Deck criado com sucesso!"),
        )

    except DatabaseInsertFailed:
        return DeckResponse(
            response=Response(success=False, message="Falha ao criar Deck!")
        )

    except TokenError as error:
        return DeckResponse(response=Response(success=False, message=str(error)))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return DeckResponse(response=Response(success=True, message="Falha ao remover Deck!"))


@deck_mutations.field("edit_deck")
@validate_token
def resolve_edit_deck(
    _, info, deck_id: int, name: str, description: str, token: dict
) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        deck_service = DeckService(session=MySQLDB().session)
        deck_user = deck_service.validate_deck_user(user_id=user_info["id"], deck_id=deck_id)
        if not deck_user:
            return Response(success=False, message="Deck não encontrado!")

        deck_service.update_deck(
            deck_id=deck_id, deck=Deck(name=name, description=description)
        )

        return Response(success=True, message="Deck atualizado com sucesso!")

    except DatabaseInsertFailed:
        return Response(success=False, message="Falha ao atualizar Deck!")

    except TokenError as error:
        return Response(success=False, message=str(error))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=True, message="Falha ao atualizar Deck!")


@deck_mutations.field("delete_deck")
@validate_token
def resolve_delete_deck(
    _, info, deck_id: int, token: dict
) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        deck_service = DeckService(session=MySQLDB().session)
        deck_user = deck_service.validate_deck_user(user_id=user_info["id"], deck_id=deck_id)
        if not deck_user:
            return Response(success=False, message="Deck não encontrado!")

        deck_service.delete_deck(deck_id=deck_id)
        return Response(success=True, message="Deck removido com sucesso!")

    except DatabaseInsertFailed:
        return Response(success=False, message="Falha ao remover Deck!")

    except TokenError as error:
        return Response(success=False, message=str(error))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=True, message="Falha ao remover Deck!")