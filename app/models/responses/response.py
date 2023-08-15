"""Response Model"""
from dataclasses import dataclass


@dataclass
class Response:
    """Modelo genérico de resposta."""

    success: bool
    message: str = None
    error: str = None
