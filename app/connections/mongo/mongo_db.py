"""MongoDB."""
from typing import Optional

from pymongo import MongoClient


class MongoDB:
    """Classe para gerenciamento do MongoDB."""

    def __init__(self, host="localhost", port=27017, db_name="Flashcards"):
        """Construtor da classe.

        Args:
            host(str): Host do MongoDB
            port(int): Port do MongoDB
            db_name(str): DB do MongoDB
        """
        self.client = MongoClient(
            host=host, port=port, username="admin", password="admin"
        )
        self.database = self.client[db_name]

    def insert_document(self, collection_name: str, document: dict):
        """Inserção de um novo registro no MongoDB.

        Args:
            collection_name (str): Nome da Collection do mongoDB
            document (dict): Documento a ser inserido no mongoDB

        Returns:
            inserted_id (int): ID do registro gerado pelo MongoDB
        """
        collection = self.database[collection_name]
        inserted_id = collection.insert_one(document).inserted_id
        return inserted_id

    def find_documents(self, collection_name: str, mongo_query: Optional[dict] = None):
        """Busca de um registro no MongoDB.

        Args:
            collection_name (str): Nome da Collection do mongoDB
            mongo_query (Optional[dict]): Query de busca no MongoDB

        Returns:
            documents (list): Lista com os registros encontrados no mongoDB
        """
        collection = self.database[collection_name]
        documents = collection.find(mongo_query) if mongo_query else collection.find()
        return list(documents)
