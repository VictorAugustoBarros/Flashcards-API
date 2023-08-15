"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.user_controller import UserController
from app.models.responses.response import Response
from app.models.responses.user_response import UserResponse
from app.models.users.user import User

user_mutation = MutationType()
user_controller = UserController()


@user_mutation.field("add_user")
def resolve_add_user(_, info, email: str, username: str, password: str) -> UserResponse:
    """Inserção de um novo usuário

    Args:
        _:
        info:
        email:
        username:
        password:

    Returns:

    """

    try:
        user_exist = user_controller.validate_user_email_username_exists(
            email=email, username=username
        )
        if user_exist:
            return UserResponse(
                response=Response(
                    success=False, message="Email ou Username já cadastrado!"
                ),
            )

        user = User(email=email, username=username, password=password)
        user_controller.insert_user(user=user)
        return UserResponse(
            user=user,
            response=Response(success=True, message="User criado com sucesso!"),
        )

    except Exception as error:
        # TODO -> Criar exception generica para Falha de inserção
        return UserResponse(
            response=Response(
                success=False, message="Falha ao criar User!", error=str(error)
            )
        )
