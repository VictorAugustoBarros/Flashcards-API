"""User Response Model."""
from dataclasses import dataclass

from app.models.responses.response import Response


@dataclass
class UserLoginResponse:
    """Modelo de resposta do UserLogin."""

    jwt_token: str = ""
    response: Response = None
