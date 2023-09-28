"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.graphql_config.models.response import Response

user_deck_mutation = MutationType()


@user_deck_mutation.field("link_user_deck")
def resolve_add_user(_, info, user_id: int, deck_id: int) -> Response:
    """Vinculo do User com o Deck

    Args:
        _:
        info:
        user_id: ID do Usuário
        deck_id: ID do Deck

    Returns:
        Response
    """
    try:
        user_exists = user_controller.validate_user_exists(user_id=user_id)
        if not user_exists:
            return Response(success=False, message="Não existe um User com esse ID!")

        deck_exists = deck_controller.validate_deck_exists(deck_id=deck_id)
        if not deck_exists:
            return Response(success=False, message="Não existe um Deck com esse ID!")

        userdeck_exists = user_deck_controller.validate_link_userdeck_exists(
            user_id=user_id, deck_id=deck_id
        )
        if userdeck_exists:
            return Response(success=False, message="Vinculo já existe!")

        user_deck_controller.insert_user_deck(user_id=user_id, deck_id=deck_id)

        return Response(success=True, message="Vinculo criado com sucesso!")

    except Exception as error:
        # TODO -> Criar exception generica para Falha de inserção
        return Response(success=False, message="Falha ao criar Vinculo!", error=error)
