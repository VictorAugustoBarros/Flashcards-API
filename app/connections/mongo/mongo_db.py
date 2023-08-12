"""MongoDB."""
from typing import Optional

from pymongo import MongoClient

from app.credencials import (
    mongo_database,
    mongo_host,
    mongo_password,
    mongo_port,
    mongo_user,
)


class MongoDB:
    """Classe para gerenciamento do MongoDB."""

    def __init__(self):
        """Construtor da classe."""
        self.mongod_db = self.connect()

    @staticmethod
    def connect():
        """Conexão com o MongoDB

        Returns:
            client[mongo_database]: Conexão com o database
        """
        client = MongoClient(
            host=mongo_host,
            port=mongo_port,
            username=mongo_user,
            password=mongo_password,
        )
        return client[mongo_database]

    def close(self):
        """Fechamento da conexão"""
        self.mongod_db.close()

    def insert_document(self, collection_name: str, document: dict) -> str:
        """Inserção de um novo registro no MongoDB.

        Args:
            collection_name (str): Nome da Collection do mongoDB
            document (dict): Documento a ser inserido no mongoDB

        Returns:
            inserted_id (int): ID do registro gerado pelo MongoDB
        """
        collection = self.mongod_db[collection_name]
        inserted_id = collection.insert_one(document=document).inserted_id
        return inserted_id

    def find_documents(self, collection_name: str, mongo_query: Optional[dict] = None):
        """Busca de um registro no MongoDB.

        Args:
            collection_name (str): Nome da Collection do mongoDB
            mongo_query (Optional[dict]): Query de busca no MongoDB

        Returns:
            documents (list): Lista com os registros encontrados no mongoDB
        """
        collection = self.mongod_db[collection_name]
        documents = (
            collection.find(filter=mongo_query) if mongo_query else collection.find()
        )
        return list(documents)

    def find_one_document(self, collection_name: str, mongo_query: dict):
        """Busca de um registro no MongoDB.

        Args:
            collection_name (str): Nome da Collection do mongoDB
            mongo_query (dict): Query de busca no MongoDB

        Returns:
            documents (list): Lista com os registros encontrados no mongoDB
        """
        collection = self.mongod_db[collection_name]
        document = collection.find_one(filter=mongo_query)
        return document
