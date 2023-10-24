from unittest import TestCase
from python_graphql_client import GraphqlClient
from app.services.card_service import CardService
from app.connections.mysql import MySQLDB
from fastapi.testclient import TestClient
from app.api import app


class TestCardMutation(TestCase):
    """Classe para testes unitário da classe CardController"""

    @classmethod
    def setUp(self) -> None:
        self.card_service = CardService(session=MySQLDB().session)

    @classmethod
    def setUpClass(self) -> None:
        self.api_client = TestClient(app)
        self.graphql_client = GraphqlClient(endpoint="http://localhost:8000/graphql/")

    def test_add_card(self):
        query = """
            mutation {
              add_card (subdeck_id: 3, question: "Hataraku", answer: "Trabalhar") {
                  card {
                    id
                  }    
                  response {
                      success
                  }    
              }
            }
        """
        result = self.client.execute(query=query)

        success = result["data"]["add_card"]["response"]["success"]
        if success:
            card_id = result["data"]["add_card"]["card"]["id"]
            self.card_service.delete_card(card_id=card_id)

        self.assertTrue(success)
