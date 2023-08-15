"""Card Query GraphQL."""
from typing import List, Union, Optional

from ariadne import QueryType
from app.models.responses.response import Response
from app.controllers.user_subdeck_controller import UserSubDeckController
from app.models.subdecks.subdeck import SubDeck

user_subdeck_query = QueryType()
user_subdeck_controller = UserSubDeckController()


@user_subdeck_query.field("get_user_subdeck")
def resolve_get_user_subdeck(
    *_, user_id: int
) -> Optional[Union[Response, List[SubDeck]]]:
    """Busca dos Subdecks do usuário

    Args:
        *_:
        user_id(int): ID do usuário

    Returns:

    """
    try:
        return user_subdeck_controller.get_user_subdeck(user_id=user_id)

    except Exception as error:
        # TODO -> Criar exception generica para Falha de inserção
        return Response(success=False, message="Falha ao criar Card!", error=str(error))
