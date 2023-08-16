"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.connections.dependencies import Dependencies
from app.controllers.user_controller import UserController
from app.models.responses.response import Response
from app.models.responses.user_response import UserResponse
from app.models.users.user import User
from app.utils.errors import DatabaseInsertFailed

user_mutation = MutationType()
db_conn = Dependencies.create_database()
user_controller = UserController(db_conn=db_conn)


@user_mutation.field("add_user")
def resolve_add_user(_, info, email: str, username: str, password: str) -> UserResponse:
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

    except DatabaseInsertFailed:
        return UserResponse(
            response=Response(success=False, error="Falha ao criar User!")
        )

    except Exception as error:
        raise error
