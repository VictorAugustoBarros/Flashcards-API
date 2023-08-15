"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.card_controller import CardController
from app.models.cards.card import Card
from app.models.responses.card_response import CardResponse
from app.models.responses.response import Response

card_mutation = MutationType()
card_controller = CardController()


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
        inserted_card = card_controller.insert_card(
            card=Card(question=question, answer=answer), subdeck_id=subdeck_id
        )
        return CardResponse(
            card=inserted_card,
            response=Response(success=True, message="Card criado com sucesso!"),
        )

    except Exception as error:
        # TODO -> Criar exception generica para Falha de inserção
        return CardResponse(
            response=Response(
                success=False, message="Falha ao criar Card!", error=str(error)
            )
        )
