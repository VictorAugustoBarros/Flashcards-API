"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.subdeck_controller import SubDeckController
from app.models.subdecks.subdeck import SubDeck

subdeck_mutation = MutationType()
subdeck_controller = SubDeckController()


@subdeck_mutation.field("add_subdeck")
def resolve_add_subdeck(_, info, deck_id: int, name: str, description: str):
    try:
        # TODO -> Validar se existe um deck com esse ID
        sub_deck = SubDeck(name=name, description=description)
        subdeck_controller.insert_subdeck(subdeck=sub_deck, deck_id=deck_id)
        return {"success": True, "message": "Subdeck criado com sucesso!"}

    except Exception as error:
        return {
            "success": False,
            "message": "Falha ao criar Subdeck!",
            "error": str(error),
        }
