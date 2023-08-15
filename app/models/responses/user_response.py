"""User Response Model."""
from dataclasses import dataclass

from app.models.responses.response import Response
from app.models.users.user import User


@dataclass
class UserResponse:
    """Modelo de resposta do User."""

    user: User = None
    response: Response = None
