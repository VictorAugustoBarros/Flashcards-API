"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.user_controller import UserController
from app.models.users.user import User

user_mutation = MutationType()
user_controller = UserController()


# TODO -> Criar uma mutation para validar se o username já existo no banco (criação usernam frontend)


@user_mutation.field("add_user")
def resolve_add_user(_, info, email: str, username: str, password: str):
    try:
        user = User(email=email, username=username, password=password)
        user_exist = user_controller.validate_user_exists(user=user)
        if not user_exist:
            user_controller.insert_user(user=user)
            return {"success": True, "message": "User criado com sucesso!"}

        return {"success": False, "message": "User já existe!"}

    except Exception as error:
        return {
            "success": False,
            "message": "Falha ao criar User!",
            "error": str(error),
        }
