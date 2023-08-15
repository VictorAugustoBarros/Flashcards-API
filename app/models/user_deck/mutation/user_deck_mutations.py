"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.deck_controller import DeckController
from app.controllers.user_controller import UserController
from app.controllers.user_deck_controller import UserDeckController

user_deck_mutation = MutationType()
user_deck_controller = UserDeckController()
user_controller = UserController()
deck_controller = DeckController()


@user_deck_mutation.field("link_user_deck")
def resolve_add_user(_, info, user_id: int, deck_id: int):
    try:
        user_exists = user_controller.validate_user_exists(user_id=user_id)
        if not user_exists:
            return {"success": False, "message": "Não existe um User com esse ID!"}

        deck_exists = deck_controller.validate_deck_exists(deck_id=deck_id)
        if not deck_exists:
            return {"success": False, "message": "Não existe um Deck com esse ID!"}

        userdeck_exists = user_deck_controller.validate_link_userdeck_exists(user_id=user_id, deck_id=deck_id)
        if userdeck_exists:
            return {"success": False, "message": "Vinculo já existe!"}

        user_deck_controller.insert_user_deck(user_id=user_id, deck_id=deck_id)

        return {"success": True, "message": "Vinculo criado com sucesso!"}

    except Exception as error:
        return {
            "success": False,
            "message": "Falha ao criar Vinculo!",
            "error": str(error),
        }
