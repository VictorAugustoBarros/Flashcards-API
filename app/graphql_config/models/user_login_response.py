"""User Response Model."""
from dataclasses import dataclass

from app.graphql_config.models.response import Response


@dataclass
class UserLoginResponse:
    """Modelo de resposta do UserLogin."""

    jwt_token: str = ""
    response: Response = None
