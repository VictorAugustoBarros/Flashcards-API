"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.connections.dependencies import Dependencies
from app.controllers.subdeck_controller import SubDeckController
from app.controllers.user_controller import UserController
from app.controllers.user_subdeck_controller import UserSubDeckController
from app.models.responses.response import Response
from app.utils.errors import DatabaseInsertFailed

user_subdeck_mutation = MutationType()
db_conn = Dependencies.create_database()

user_subdeck_controller = UserSubDeckController(db_conn=db_conn)
user_controller = UserController(db_conn=db_conn)
subdeck_controller = SubDeckController(db_conn=db_conn)


@user_subdeck_mutation.field("link_user_subdeck")
def resolve_add_user(_, info, user_id: int, subdeck_id: int) -> Response:
    """Criando o vinculo entre o User e o Subdeck

    Args:
        _:
        info:
        user_id(int): ID do usuário
        subdeck_id(int): ID do Subdeck

    Returns:
        Response:

    """
    try:
        user_exists = user_controller.validate_user_exists(user_id=user_id)
        if not user_exists:
            return Response(success=False, message="Não existe um User com esse ID!")

        deck_exists = subdeck_controller.validate_subdeck_exists(subdeck_id=subdeck_id)
        if not deck_exists:
            return Response(success=False, message="Não existe um Deck com esse ID!")

        usersubdeck_exists = user_subdeck_controller.validate_link_userdeck_exists(
            user_id=user_id, subdeck_id=subdeck_id
        )
        if usersubdeck_exists:
            return Response(success=False, message="Vinculo já existe!")

        user_subdeck_controller.insert_user_subdeck(
            user_id=user_id, subdeck_id=subdeck_id
        )

        return Response(success=True, message="Vinculo criado com sucesso!")

    except DatabaseInsertFailed:
        return Response(success=False, error="Falha ao criar Vinculo!")

    except Exception as error:
        raise error
