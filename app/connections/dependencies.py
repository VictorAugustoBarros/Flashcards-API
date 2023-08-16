"""Dependency Injection."""
from dataclasses import dataclass

from app.connections.mysql.mysql_db import MySQLDB


@dataclass
class Dependencies:
    """Classe para Injeção de dependencias."""

    @staticmethod
    def create_database():
        return MySQLDB()
