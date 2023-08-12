"""Dependency Injection."""
from typing import Union
from app.connections.mongo.mongo_db import MongoDB


def get_database() -> Union[MongoDB, ]:
    """Retorno do database a ser utlizado

    Returns:
        mongo_db (MongoDB): Conexão com o database
    """
    mongo_db = MongoDB()
    return mongo_db
