"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.connections.dependencies import Dependencies
from app.controllers.card_controller import CardController
from app.controllers.subdeck_controller import SubDeckController
from app.models.cards.card import Card
from app.models.responses.card_response import CardResponse
from app.models.responses.response import Response
from app.utils.errors import DatabaseInsertFailed, DatabaseQueryFailed

card_mutation = MutationType()
db_conn = Dependencies().create_database()
card_controller = CardController(db_conn=db_conn)
subdeck_controller = SubDeckController(db_conn=db_conn)


@card_mutation.field("add_card")
def resolve_add_card(
    _, info, subdeck_id: int, question: str, answer: str
) -> CardResponse:
    """Inserção de um novo Card

    Args:
        _:
        info:
        subdeck_id(int): ID do Subdeck
        question(str): Pergunta do Card
        answer(str): Resposta do Card

    Returns:
        Response: Resposta do sucesso da operação
    """
    try:
        sudeck_exists = subdeck_controller.validate_subdeck_exists(
            subdeck_id=subdeck_id
        )
        if not sudeck_exists:
            return CardResponse(
                response=Response(
                    success=False, message="Não existe um SubDeck com esse ID!"
                )
            )

        inserted_card = card_controller.insert_card(
            card=Card(question=question, answer=answer), subdeck_id=subdeck_id
        )
        return CardResponse(
            card=inserted_card,
            response=Response(success=True, message="Card criado com sucesso!"),
        )

    except (DatabaseInsertFailed, DatabaseQueryFailed):
        return CardResponse(
            response=Response(success=False, error="Falha ao criar Card!")
        )

    except Exception as error:
        raise error
