"""Card Query GraphQL."""
from ariadne import QueryType

from app.controllers.user_controller import UserController

user_query = QueryType()
user_controller = UserController()


@user_query.field("get_user")
def resolve_get_users(*_, user_id: int):
    users = user_controller.get_user(user_id=user_id)

    return users


@user_query.field("get_users")
def resolve_get_users(*_):
    users = user_controller.get_all_users()

    return users


@user_query.field("validate_username")
def resolve_validate_username(*_, username: str):
    username = user_controller.validate_username_exists(username=username)
    if username:
        return {"success": False, "message": "Username já existe!"}

    return {"success": True, "message": "Username disponível!"}
