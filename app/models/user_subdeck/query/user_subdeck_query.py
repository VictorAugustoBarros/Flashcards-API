"""Card Query GraphQL."""
from typing import List, Optional, Union

from ariadne import QueryType

from app.connections.dependencies import Dependencies
from app.controllers.user_subdeck_controller import UserSubDeckController
from app.models.responses.response import Response
from app.models.subdecks.subdeck import SubDeck

user_subdeck_query = QueryType()
db_conn = Dependencies.create_database()
user_subdeck_controller = UserSubDeckController(db_conn=db_conn)


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
