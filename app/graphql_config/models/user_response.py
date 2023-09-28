"""User Response Model."""
from dataclasses import dataclass

from app.graphql_config.models.response import Response
from app.models.user import User


@dataclass
class UserResponse:
    """Modelo de resposta do User."""

    user: User = None
    response: Response = None
