"""Card Mutations GraphQL."""

from ariadne import MutationType

from app.controllers.deck_controller import DeckController
from app.controllers.user_deck_controller import UserDeckController
from app.models.deck import Deck
from app.graphql_config.models.deck_response import DeckResponse
from app.graphql_config.models.response import Response
from app.utils.errors import DatabaseInsertFailed, TokenError
from app.validations.middleware_validation import validate_token

deck_mutation = MutationType()


@deck_mutation.field("add_deck")
@validate_token
def resolve_add_deck(_, info, name: str, description: str, token: dict) -> DeckResponse:
    """Inserção de um novo Deck

    Args:
        _:
        info: Informações sobre a request
        name: Nome do Deck
        description: Descrição do Deck
        token: Token valido?

    Returns:
        DeckResponse
    """
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        db_conn = Dependencies.create_database()

        deck_controller = DeckController(db_conn=db_conn)
        inserted_deck = deck_controller.insert_deck(
            deck=Deck(name=name, description=description)
        )

        user_deck_controller = UserDeckController(db_conn=db_conn)
        user_deck_controller.insert_user_deck(
            user_id=user_info["id"], deck_id=inserted_deck.id
        )

        return DeckResponse(
            deck=inserted_deck,
            response=Response(success=True, message="Deck criado com sucesso!"),
        )

    except DatabaseInsertFailed:
        return DeckResponse(
            response=Response(success=False, error="Falha ao criar Deck!")
        )

    except TokenError as error:
        return DeckResponse(response=Response(success=False, error=str(error)))

    except Exception as error:
        raise error
