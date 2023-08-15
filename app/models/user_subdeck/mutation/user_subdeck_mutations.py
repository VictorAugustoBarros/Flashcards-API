"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.subdeck_controller import SubDeckController
from app.controllers.user_controller import UserController
from app.controllers.user_subdeck_controller import UserSubDeckController

user_subdeck_mutation = MutationType()
user_subdeck_controller = UserSubDeckController()
user_controller = UserController()
subdeck_controller = SubDeckController()


@user_subdeck_mutation.field("link_user_subdeck")
def resolve_add_user(_, info, user_id: int, subdeck_id: int):
    try:
        user_exists = user_controller.validate_user_exists(user_id=user_id)
        if not user_exists:
            return {"success": False, "message": "Não existe um User com esse ID!"}

        deck_exists = subdeck_controller.validate_subdeck_exists(subdeck_id=subdeck_id)
        if not deck_exists:
            return {"success": False, "message": "Não existe um Deck com esse ID!"}

        usersubdeck_exists = user_subdeck_controller.validate_link_userdeck_exists(user_id=user_id, subdeck_id=subdeck_id)
        if usersubdeck_exists:
            return {"success": False, "message": "Vinculo já existe!"}

        user_subdeck_controller.insert_user_subdeck(
            user_id=user_id, subdeck_id=subdeck_id
        )

        return {"success": True, "message": "Vinculo criado com sucesso!"}

    except Exception as error:
        return {
            "success": False,
            "message": "Falha ao criar Vinculo!",
            "error": str(error),
        }
